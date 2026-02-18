import { useState, useRef, useEffect } from 'react'
import { motion } from 'framer-motion'
import WaveSurfer from 'wavesurfer.js'

export default function AudioVisualizer({ isActive, onAudioData }) {
    const containerRef = useRef(null)
    const wavesurferRef = useRef(null)
    const mediaRecorderRef = useRef(null)
    const [audioLevel, setAudioLevel] = useState(0)

    useEffect(() => {
        if (containerRef.current && !wavesurferRef.current) {
            // Initialize WaveSurfer for visualization
            wavesurferRef.current = WaveSurfer.create({
                container: containerRef.current,
                waveColor: '#00ff9f',
                progressColor: '#ff006e',
                cursorColor: '#ffbe0b',
                barWidth: 3,
                barRadius: 3,
                barGap: 2,
                height: 128,
                normalize: true,
                backend: 'WebAudio',
            })
        }

        return () => {
            if (wavesurferRef.current) {
                wavesurferRef.current.destroy()
            }
        }
    }, [])

    useEffect(() => {
        if (isActive) {
            startRecording()
        } else {
            stopRecording()
        }
    }, [isActive])

    const startRecording = async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true })

            // Use MediaRecorder to capture audio chunks
            mediaRecorderRef.current = new MediaRecorder(stream)

            mediaRecorderRef.current.ondataavailable = (event) => {
                if (event.data.size > 0 && onAudioData) {
                    onAudioData(event.data)
                }
            }

            // Start recording, emit data every 2 seconds
            mediaRecorderRef.current.start(2000)

            // Connect to WaveSurfer for visualization
            if (wavesurferRef.current) {
                wavesurferRef.current.loadMediaStream(stream)

                // Animate audio level
                const audioContext = new AudioContext()
                const source = audioContext.createMediaStreamSource(stream)
                const analyser = audioContext.createAnalyser()
                source.connect(analyser)

                const dataArray = new Uint8Array(analyser.frequencyBinCount)

                const updateLevel = () => {
                    if (isActive) {
                        analyser.getByteFrequencyData(dataArray)
                        const average = dataArray.reduce((a, b) => a + b) / dataArray.length
                        setAudioLevel(average / 255)
                        requestAnimationFrame(updateLevel)
                    }
                }
                updateLevel()
            }

            console.log('🎤 Recording started')
        } catch (error) {
            console.error('Microphone access denied:', error)
            alert('Please allow microphone access to use the visualizer.')
        }
    }

    const stopRecording = () => {
        if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
            mediaRecorderRef.current.stop()

            // Stop all tracks
            mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop())

            console.log('🛑 Recording stopped')
        }

        setAudioLevel(0)
    }

    return (
        <div className="h-full flex flex-col p-6 bg-dino-surface border border-dino-primary/20 rounded-lg">
            {/* Header */}
            <div className="mb-4">
                <h2 className="text-2xl font-cyber font-bold text-dino-primary mb-2">
                    AUDIO INPUT
                </h2>
                <div className="flex items-center gap-2">
                    <div className={`status-dot ${isActive ? 'active' : 'inactive'}`}></div>
                    <span className="text-sm text-dino-text-dim font-mono">
                        {isActive ? 'LISTENING...' : 'IDLE'}
                    </span>
                </div>
            </div>

            {/* Waveform */}
            <div className="flex-1 flex items-center justify-center">
                <div ref={containerRef} className="w-full waveform-container"></div>
            </div>

            {/* Audio Level Meter */}
            <div className="mt-4">
                <div className="flex items-center justify-between mb-2">
                    <span className="text-xs text-dino-text-dim font-mono">LEVEL</span>
                    <span className="text-xs text-dino-primary font-mono">
                        {(audioLevel * 100).toFixed(0)}%
                    </span>
                </div>
                <div className="h-2 bg-dino-background rounded-full overflow-hidden">
                    <motion.div
                        className="h-full bg-gradient-to-r from-dino-primary via-dino-accent to-dino-secondary"
                        initial={{ width: 0 }}
                        animate={{ width: `${audioLevel * 100}%` }}
                        transition={{ duration: 0.1 }}
                        style={{
                            boxShadow: `0 0 10px rgba(0, 255, 159, ${audioLevel})`
                        }}
                    />
                </div>
            </div>

            {/* Stats */}
            {isActive && (
                <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="mt-4 grid grid-cols-2 gap-2"
                >
                    <div className="p-2 bg-dino-background/50 rounded border border-dino-primary/10">
                        <div className="text-xs text-dino-text-dim font-mono">FORMAT</div>
                        <div className="text-sm text-dino-text font-mono">WEBM/OPUS</div>
                    </div>
                    <div className="p-2 bg-dino-background/50 rounded border border-dino-primary/10">
                        <div className="text-xs text-dino-text-dim font-mono">RATE</div>
                        <div className="text-sm text-dino-text font-mono">48kHz</div>
                    </div>
                </motion.div>
            )}
        </div>
    )
}
