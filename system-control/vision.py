"""
👁️ Sophia Ghost in the Shell - Vision Module
STAGE 3: Awareness & Vision - See the World

This module gives Sophia the power to see and respond to visual stimuli.
Screenshot capture, OCR text recognition, and image analysis capabilities.
"""

import os
import io
import time
import json
from datetime import datetime
from typing import Tuple, Dict, List, Optional, Any
from PIL import Image, ImageGrab, ImageEnhance, ImageDraw
import numpy as np

# OCR will be imported conditionally
try:
    import pytesseract
    OCR_AVAILABLE = True
    print("✅ OCR capabilities available")
except ImportError:
    OCR_AVAILABLE = False
    print("⚠️ OCR not available - install: pip install pytesseract")

# OpenCV for advanced image processing (optional)
try:
    import cv2
    CV2_AVAILABLE = True
    print("✅ Advanced image processing available")
except ImportError:
    CV2_AVAILABLE = False
    print("⚠️ OpenCV not available - install: pip install opencv-python")

class Vision:
    """Advanced vision system for screen awareness and image processing"""
    
    def __init__(self, screenshots_dir: str = "screenshots"):
        self.screenshots_dir = screenshots_dir
        self.screenshot_history = []
        self.ocr_cache = {}
        
        # Create screenshots directory
        os.makedirs(screenshots_dir, exist_ok=True)
        
        # Screen dimensions
        try:
            test_screenshot = ImageGrab.grab()
            self.screen_width, self.screen_height = test_screenshot.size
            print(f"👁️ Vision initialized - Screen: {self.screen_width}x{self.screen_height}")
        except Exception as e:
            print(f"⚠️ Could not determine screen size: {e}")
            self.screen_width, self.screen_height = 1920, 1080  # Default
        
        # Configure OCR if available
        if OCR_AVAILABLE:
            self._configure_ocr()
    
    def _configure_ocr(self):
        """Configure OCR settings for better accuracy"""
        try:
            # Test OCR configuration
            test_image = Image.new('RGB', (100, 50), color='white')
            pytesseract.image_to_string(test_image, config='--psm 6')
            print("🔤 OCR configuration verified")
        except Exception as e:
            print(f"⚠️ OCR configuration issue: {e}")
    
    def capture_screen(self, region: Optional[Tuple[int, int, int, int]] = None, 
                      save: bool = False, filename: Optional[str] = None) -> Dict[str, Any]:
        """
        Capture screenshot of entire screen or specific region
        
        Args:
            region: (left, top, right, bottom) coordinates for partial capture
            save: Whether to save the screenshot to disk
            filename: Custom filename for saved screenshot
        """
        try:
            # Capture screenshot
            if region:
                screenshot = ImageGrab.grab(bbox=region)
            else:
                screenshot = ImageGrab.grab()
            
            result = {
                "status": "success",
                "timestamp": datetime.now().isoformat(),
                "size": screenshot.size,
                "mode": screenshot.mode,
                "region": region
            }
            
            # Save if requested
            if save:
                if not filename:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"screenshot_{timestamp}.png"
                
                filepath = os.path.join(self.screenshots_dir, filename)
                screenshot.save(filepath)
                result["saved_path"] = filepath
                print(f"📸 Screenshot saved: {filepath}")
            
            # Add to history
            history_entry = {
                "timestamp": result["timestamp"],
                "size": screenshot.size,
                "region": region,
                "saved": save,
                "filename": filename if save else None
            }
            
            self.screenshot_history.append(history_entry)
            
            # Keep history manageable
            if len(self.screenshot_history) > 50:
                self.screenshot_history = self.screenshot_history[-25:]
            
            # Store the image object in result for further processing
            result["image"] = screenshot
            
            return result
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def read_text_from_screen(self, region: Optional[Tuple[int, int, int, int]] = None,
                            language: str = 'eng', config: str = '--psm 6') -> Dict[str, Any]:
        """
        Extract text from screen using OCR
        
        Args:
            region: Optional region to scan (left, top, right, bottom)
            language: OCR language (default: 'eng')
            config: Tesseract configuration string
        """
        if not OCR_AVAILABLE:
            return {
                "status": "error",
                "error": "OCR not available - install pytesseract"
            }
        
        try:
            # Capture screen
            capture_result = self.capture_screen(region=region)
            if capture_result["status"] == "error":
                return capture_result
            
            screenshot = capture_result["image"]
            
            # Check cache for identical images (basic optimization)
            cache_key = f"{screenshot.size}_{region}_{config}"
            
            # Enhance image for better OCR
            enhanced_image = self._enhance_for_ocr(screenshot)
            
            # Perform OCR
            text = pytesseract.image_to_string(enhanced_image, lang=language, config=config)
            
            # Get detailed OCR data
            detailed_data = pytesseract.image_to_data(enhanced_image, lang=language, config=config, output_type=pytesseract.Output.DICT)
            
            # Process and clean text
            cleaned_text = self._clean_ocr_text(text)
            
            result = {
                "status": "success",
                "text": cleaned_text,
                "raw_text": text,
                "word_count": len(cleaned_text.split()),
                "character_count": len(cleaned_text),
                "region": region,
                "language": language,
                "config": config,
                "timestamp": datetime.now().isoformat(),
                "confidence_scores": detailed_data.get('conf', []),
                "word_details": self._extract_word_details(detailed_data)
            }
            
            # Cache result
            self.ocr_cache[cache_key] = result
            
            return result
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def find_text_on_screen(self, search_text: str, region: Optional[Tuple[int, int, int, int]] = None,
                          case_sensitive: bool = False) -> Dict[str, Any]:
        """
        Search for specific text on screen and return its location
        """
        try:
            ocr_result = self.read_text_from_screen(region=region)
            if ocr_result["status"] == "error":
                return ocr_result
            
            text_to_search = ocr_result["text"]
            search_term = search_text if case_sensitive else search_text.lower()
            text_content = text_to_search if case_sensitive else text_to_search.lower()
            
            found = search_term in text_content
            
            result = {
                "status": "success",
                "found": found,
                "search_text": search_text,
                "case_sensitive": case_sensitive,
                "full_text": text_to_search,
                "word_count": ocr_result["word_count"],
                "timestamp": datetime.now().isoformat()
            }
            
            if found:
                # Try to find approximate position
                word_details = ocr_result.get("word_details", [])
                matching_words = []
                
                for word_info in word_details:
                    word_text = word_info["text"]
                    if not case_sensitive:
                        word_text = word_text.lower()
                    
                    if search_term in word_text:
                        matching_words.append(word_info)
                
                result["matches"] = matching_words
                result["match_count"] = len(matching_words)
            
            return result
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def find_buttons_and_controls(self, region: Optional[Tuple[int, int, int, int]] = None) -> Dict[str, Any]:
        """
        Find common UI buttons and controls on screen
        """
        common_buttons = [
            "OK", "Cancel", "Yes", "No", "Apply", "Close", "Save", "Open",
            "Submit", "Continue", "Next", "Previous", "Back", "Finish",
            "Start", "Stop", "Play", "Pause", "Settings", "Options"
        ]
        
        try:
            ocr_result = self.read_text_from_screen(region=region)
            if ocr_result["status"] == "error":
                return ocr_result
            
            found_controls = []
            
            for button_text in common_buttons:
                search_result = self.find_text_on_screen(button_text, region=region, case_sensitive=False)
                if search_result.get("found", False):
                    found_controls.append({
                        "button_text": button_text,
                        "matches": search_result.get("matches", [])
                    })
            
            return {
                "status": "success",
                "found_controls": found_controls,
                "control_count": len(found_controls),
                "searched_buttons": common_buttons,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def analyze_screen_layout(self, region: Optional[Tuple[int, int, int, int]] = None) -> Dict[str, Any]:
        """
        Analyze overall screen layout and structure
        """
        try:
            # Capture screen
            capture_result = self.capture_screen(region=region)
            if capture_result["status"] == "error":
                return capture_result
            
            screenshot = capture_result["image"]
            
            # Basic image analysis
            analysis = {
                "status": "success",
                "image_size": screenshot.size,
                "mode": screenshot.mode,
                "timestamp": datetime.now().isoformat()
            }
            
            # Color analysis
            if screenshot.mode == 'RGB':
                # Convert to numpy array for analysis
                img_array = np.array(screenshot)
                
                # Calculate basic statistics
                analysis["color_stats"] = {
                    "mean_rgb": img_array.mean(axis=(0, 1)).tolist(),
                    "std_rgb": img_array.std(axis=(0, 1)).tolist()
                }
                
                # Detect if image is mostly light or dark
                grayscale = img_array.mean(axis=2)
                mean_brightness = grayscale.mean()
                analysis["brightness"] = {
                    "average": float(mean_brightness),
                    "theme": "light" if mean_brightness > 127 else "dark"
                }
            
            # OCR analysis for text regions
            if OCR_AVAILABLE:
                ocr_result = self.read_text_from_screen(region=region)
                if ocr_result["status"] == "success":
                    analysis["text_analysis"] = {
                        "word_count": ocr_result["word_count"],
                        "character_count": ocr_result["character_count"],
                        "has_text": ocr_result["word_count"] > 0
                    }
            
            return analysis
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def _enhance_for_ocr(self, image: Image.Image) -> Image.Image:
        """Enhance image for better OCR accuracy"""
        try:
            # Convert to grayscale
            if image.mode != 'L':
                image = image.convert('L')
            
            # Enhance contrast
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(2.0)
            
            # Enhance sharpness
            enhancer = ImageEnhance.Sharpness(image)
            image = enhancer.enhance(1.5)
            
            return image
            
        except Exception:
            return image
    
    def _clean_ocr_text(self, text: str) -> str:
        """Clean and normalize OCR text output"""
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Remove common OCR artifacts
        artifacts = ['|', '~', '^', '_']
        for artifact in artifacts:
            text = text.replace(artifact, '')
        
        return text.strip()
    
    def _extract_word_details(self, ocr_data: Dict) -> List[Dict[str, Any]]:
        """Extract detailed word information from OCR data"""
        word_details = []
        
        try:
            for i, text in enumerate(ocr_data.get('text', [])):
                if text.strip():  # Only include non-empty text
                    word_info = {
                        "text": text,
                        "confidence": ocr_data['conf'][i] if i < len(ocr_data['conf']) else 0,
                        "left": ocr_data['left'][i] if i < len(ocr_data['left']) else 0,
                        "top": ocr_data['top'][i] if i < len(ocr_data['top']) else 0,
                        "width": ocr_data['width'][i] if i < len(ocr_data['width']) else 0,
                        "height": ocr_data['height'][i] if i < len(ocr_data['height']) else 0
                    }
                    
                    # Calculate center point
                    word_info["center_x"] = word_info["left"] + word_info["width"] // 2
                    word_info["center_y"] = word_info["top"] + word_info["height"] // 2
                    
                    word_details.append(word_info)
        
        except Exception as e:
            print(f"⚠️ Error extracting word details: {e}")
        
        return word_details
    
    def get_screenshot_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent screenshot history"""
        return self.screenshot_history[-limit:] if self.screenshot_history else []
    
    def clear_cache(self):
        """Clear OCR cache"""
        self.ocr_cache.clear()
        print("🧹 OCR cache cleared")
    
    def get_vision_stats(self) -> Dict[str, Any]:
        """Get vision system statistics"""
        return {
            "ocr_available": OCR_AVAILABLE,
            "cv2_available": CV2_AVAILABLE,
            "screen_size": [self.screen_width, self.screen_height],
            "screenshots_taken": len(self.screenshot_history),
            "ocr_cache_size": len(self.ocr_cache),
            "screenshots_directory": self.screenshots_dir
        }

# Test function for development
def test_vision():
    """Test the vision functionality"""
    print("🧪 Testing Vision Module...")
    
    vision = Vision()
    
    # Test screenshot
    print("📸 Testing screenshot capture...")
    result = vision.capture_screen(save=True)
    print(f"Screenshot result: {result.get('status', 'unknown')}")
    
    # Test OCR if available
    if OCR_AVAILABLE:
        print("🔤 Testing OCR...")
        ocr_result = vision.read_text_from_screen()
        print(f"OCR found {ocr_result.get('word_count', 0)} words")
    
    # Test stats
    stats = vision.get_vision_stats()
    print(f"📊 Vision stats: {json.dumps(stats, indent=2)}")
    
    print("✅ Vision test completed")

if __name__ == "__main__":
    test_vision()
