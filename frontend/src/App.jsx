import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { useWebSocket } from './hooks/useWebSocket'
import AudioVisualizer from './components/AudioVisualizer'
import VideoPlayer from './components/VideoPlayer'
import Controls from './components/Controls'

function App() {
    const [isActive, setIsActive] = useState(false)
    const [videoUrl, setVideoUrl] = useState(null)
    const [jobStatus, setJobStatus] = useState(null)
    const [currentJobId, setCurrentJobId] = useState(null)
    const [energyLevel, setEnergyLevel] = useState(null)

    const {
        isConnected,
        lastMessage,
        connect,
        disconnect,
        sendAudio
    } = useWebSocket()

    // Handle WebSocket messages
    useEffect(() => {
        if (!lastMessage) return

        console.log('Processing message:', lastMessage)

        switch (lastMessage.type) {
            case 'connected':
                console.log('✅ Connected to Synesthesia Engine')
                break

            case 'analysis':
                console.log('📊 Audio features:', lastMessage.features)
                break

            case 'prompt':
                console.log('🎨 Generated prompt:', lastMessage.prompt)
                setEnergyLevel(lastMessage.energy_level)
                break

            case 'generation_started':
                console.log('🚀 Generation started:', lastMessage.job_id)
                setCurrentJobId(lastMessage.job_id)
                setJobStatus('processing')
                break

            case 'generation_complete':
                console.log('✅ Generation complete:', lastMessage)
                setJobStatus(lastMessage.status)
                if (lastMessage.video_url) {
                    setVideoUrl(lastMessage.video_url)
                }
                break

            case 'error':
                console.error('❌ Error:', lastMessage.message)
                alert(`Error: ${lastMessage.message}`)
                break
        }
    }, [lastMessage])

    const handleStart = () => {
        console.log('🎙️ Starting audio stream...')
        connect()
        setIsActive(true)
    }

    const handleStop = () => {
        console.log('🛑 Stopping audio stream...')
        disconnect()
        setIsActive(false)
    }

    const handleAudioData = (audioBlob) => {
        if (isConnected && isActive) {
            console.log('📤 Sending audio chunk:', audioBlob.size, 'bytes')
            sendAudio(audioBlob)
        }
    }

    return (
        <div className="h-screen w-screen flex flex-col bg-dino-background text-dino-text overflow-hidden">
            {/* Header */}
            <motion.header
                className="p-6 border-b border-dino-primary/20 bg-dino-surface/50 backdrop-blur-sm"
                initial={{ y: -100 }}
                animate={{ y: 0 }}
                transition={{ type: 'spring', stiffness: 100 }}
            >
                <div className="max-w-7xl mx-auto flex items-center justify-between">
                    <div>
                        <h1 className="text-4xl font-cyber font-black text-dino-primary mb-1 tracking-wider">
                            SYNESTHESIA ENGINE
                        </h1>
                        <p className="text-sm text-dino-text-dim font-mono">
                            Audio-Reactive Visual Generation • Powered by Odyssey ML
                        </p>
                    </div>

                    <div className="flex items-center gap-4">
                        <div className="text-right">
                            <div className="text-xs text-dino-text-dim font-mono">PROJECT</div>
                            <div className="text-lg font-cyber text-dino-accent">DINO 26</div>
                        </div>
                        <div className="w-16 h-16 bg-gradient-to-br from-dino-primary via-dino-accent to-dino-secondary rounded-lg flex items-center justify-center text-3xl">
                            🦖
                        </div>
                    </div>
                </div>
            </motion.header>

            {/* Main Content - Split Screen */}
            <div className="flex-1 grid grid-cols-2 gap-4 p-4 overflow-hidden">
                {/* Left Panel: Audio Visualizer */}
                <motion.div
                    initial={{ x: -100, opacity: 0 }}
                    animate={{ x: 0, opacity: 1 }}
                    transition={{ delay: 0.2 }}
                    className="h-full"
                >
                    <AudioVisualizer
                        isActive={isActive}
                        onAudioData={handleAudioData}
                    />
                </motion.div>

                {/* Right Panel: Video Player */}
                <motion.div
                    initial={{ x: 100, opacity: 0 }}
                    animate={{ x: 0, opacity: 1 }}
                    transition={{ delay: 0.3 }}
                    className="h-full"
                >
                    <VideoPlayer
                        videoUrl={videoUrl}
                        status={jobStatus}
                        jobId={currentJobId}
                    />
                </motion.div>
            </div>

            {/* Footer Controls */}
            <motion.div
                initial={{ y: 100, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.4 }}
            >
                <Controls
                    isActive={isActive}
                    onStart={handleStart}
                    onStop={handleStop}
                    connectionStatus={isConnected ? 'connected' : 'disconnected'}
                    energyLevel={energyLevel}
                />
            </motion.div>

            {/* Version Badge */}
            <div className="fixed bottom-4 right-4 text-xs text-dino-text-dim font-mono opacity-50">
                v1.0.0-poc
            </div>
        </div>
    )
}

export default App
