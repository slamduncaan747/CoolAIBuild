// Wait for the document to load before running the script
document.addEventListener('DOMContentLoaded', () => {
    const audioElement = document.querySelector('audio');
    const canvas = document.getElementById('visualizer');
    const canvasCtx = canvas.getContext('2d');
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    const analyser = audioCtx.createAnalyser();

    // Connect the audio source to the analyser
    const source = audioCtx.createMediaElementSource(audioElement);
    source.connect(analyser);
    analyser.connect(audioCtx.destination);

    // Set the analyser parameters
    analyser.fftSize = 256;
    const bufferLength = analyser.frequencyBinCount;
    const dataArray = new Uint8Array(bufferLength);

    // Draw the visualizer
    function drawVisualizer() {
        analyser.getByteFrequencyData(dataArray);

        // Clear the canvas
        canvasCtx.clearRect(0, 0, canvas.width, canvas.height);

        const barWidth = (canvas.width / bufferLength) * 2;
        let x = 0;

        dataArray.forEach(value => {
            const barHeight = value;
            const r = barHeight + (25 * (x / bufferLength));
            const g = 250 * (x / bufferLength);
            const b = 50;

            canvasCtx.fillStyle = `rgb(${r},${g},${b})`;
            canvasCtx.fillRect(x, canvas.height - barHeight, barWidth, barHeight);

            x += barWidth + 1;
        });

        requestAnimationFrame(drawVisualizer);
    }

    // Start drawing the visualizer when audio starts playing
    audioElement.addEventListener('play', () => {
        audioCtx.resume().then(() => {
            drawVisualizer();
        });
    });
});
