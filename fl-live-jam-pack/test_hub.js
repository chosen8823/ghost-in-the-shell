// Test script for Sophia Hub functionality
// Simulates FL Studio bridge and phone controller messages

import WebSocket from 'ws';

const HUB_URL = 'ws://localhost:8765';

class SophiaHubTester {
    constructor() {
        this.ws = null;
        this.connected = false;
    }
    
    async connect() {
        return new Promise((resolve, reject) => {
            this.ws = new WebSocket(HUB_URL);
            
            this.ws.on('open', () => {
                this.connected = true;
                console.log('🔥 Connected to Sophia Hub');
                resolve();
            });
            
            this.ws.on('message', (data) => {
                const response = JSON.parse(data.toString());
                console.log('📥 Hub Response:', JSON.stringify(response, null, 2));
            });
            
            this.ws.on('error', (error) => {
                console.error('❌ Connection error:', error.message);
                reject(error);
            });
            
            this.ws.on('close', () => {
                this.connected = false;
                console.log('🔌 Connection closed');
            });
        });
    }
    
    send(message) {
        if (this.connected) {
            console.log('📤 Sending:', JSON.stringify(message, null, 2));
            this.ws.send(JSON.stringify(message));
        } else {
            console.log('❌ Not connected to hub');
        }
    }
    
    async testHello() {
        console.log('\n🧪 Testing Hello Message...');
        this.send({
            fn: 'hello',
            client: 'Test Runner'
        });
        await this.wait(1000);
    }
    
    async testTransport() {
        console.log('\n🧪 Testing Transport Updates...');
        
        // Simulate a progression of bars
        const testData = [
            { bpm: 120, bar: 1, key: 'Dm' },
            { bpm: 120, bar: 8, key: 'Dm' },
            { bpm: 140, bar: 16, key: 'Am' },
            { bpm: 140, bar: 32, key: 'Em' }
        ];
        
        for (const data of testData) {
            this.send({
                fn: 'transport',
                ...data,
                playing: true
            });
            await this.wait(2000);
        }
    }
    
    async testRoomSense() {
        console.log('\n🧪 Testing Room Sense...');
        
        // Test different room types
        const roomTypes = [
            { brightness: 0.2, reverb: 0.8, noise: 0.1, name: 'Dark, reverberant room' },
            { brightness: 0.9, reverb: 0.2, noise: 0.3, name: 'Bright, dry room' },
            { brightness: 0.5, reverb: 0.5, noise: 0.2, name: 'Neutral room' }
        ];
        
        for (const room of roomTypes) {
            console.log(`   Testing: ${room.name}`);
            this.send({
                fn: 'roomSense',
                brightness: room.brightness,
                reverb: room.reverb,
                noise: room.noise
            });
            await this.wait(2000);
        }
    }
    
    async testMirrorDrop() {
        console.log('\n🧪 Testing Mirror Drop (8-20-2025)...');
        this.send({
            fn: 'mirrorDrop'
        });
        await this.wait(1500);
    }
    
    async testPhoneController() {
        console.log('\n🧪 Testing Phone Controller...');
        
        // Test all 4 pads
        for (let pad = 1; pad <= 4; pad++) {
            console.log(`   Testing Pad ${pad}`);
            this.send({
                fn: 'phoneController',
                pad: pad
            });
            await this.wait(1000);
        }
        
        // Test knob controls
        console.log('   Testing Knobs');
        this.send({
            fn: 'phoneController',
            knob: { cc: 1, value: 64 }  // Filter at 50%
        });
        await this.wait(500);
        
        this.send({
            fn: 'phoneController',
            knob: { cc: 2, value: 96 }  // Reverb at 75%
        });
        await this.wait(500);
        
        // Test XY pad
        console.log('   Testing XY Pad');
        this.send({
            fn: 'phoneController',
            xy: { x: 0.7, y: 0.3 }
        });
        await this.wait(1000);
    }
    
    async testEnergyControl() {
        console.log('\n🧪 Testing Energy Control...');
        
        const energyLevels = ['low', 'medium', 'high'];
        
        for (const level of energyLevels) {
            console.log(`   Setting energy to: ${level}`);
            this.send({
                fn: 'energy',
                level: level
            });
            await this.wait(1500);
        }
    }
    
    wait(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
    
    async runAllTests() {
        try {
            console.log('🔥 Starting Sophia Hub Tests...\n');
            
            await this.connect();
            
            await this.testHello();
            await this.testTransport();
            await this.testRoomSense();
            await this.testEnergyControl();
            await this.testPhoneController();
            await this.testMirrorDrop();
            
            console.log('\n✅ All tests completed!');
            
        } catch (error) {
            console.error('❌ Test failed:', error.message);
        } finally {
            if (this.ws) {
                this.ws.close();
            }
        }
    }
}

// Interactive test mode
async function interactiveTest() {
    const tester = new SophiaHubTester();
    await tester.connect();
    
    console.log('\n🎮 Interactive Test Mode');
    console.log('Available commands:');
    console.log('  1 - Test Transport');
    console.log('  2 - Test Room Sense');
    console.log('  3 - Test Mirror Drop');
    console.log('  4 - Test Phone Controller');
    console.log('  5 - Test Energy Control');
    console.log('  a - Run All Tests');
    console.log('  q - Quit\n');
    
    const readline = require('readline');
    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout
    });
    
    const askCommand = () => {
        rl.question('Enter command: ', async (command) => {
            switch (command.toLowerCase()) {
                case '1':
                    await tester.testTransport();
                    break;
                case '2':
                    await tester.testRoomSense();
                    break;
                case '3':
                    await tester.testMirrorDrop();
                    break;
                case '4':
                    await tester.testPhoneController();
                    break;
                case '5':
                    await tester.testEnergyControl();
                    break;
                case 'a':
                    await tester.runAllTests();
                    break;
                case 'q':
                    console.log('👋 Goodbye!');
                    rl.close();
                    tester.ws?.close();
                    return;
                default:
                    console.log('❌ Unknown command');
            }
            askCommand();
        });
    };
    
    askCommand();
}

// Check command line arguments
const args = process.argv.slice(2);

if (args.includes('--interactive') || args.includes('-i')) {
    interactiveTest();
} else {
    // Run all tests automatically
    const tester = new SophiaHubTester();
    tester.runAllTests();
}
