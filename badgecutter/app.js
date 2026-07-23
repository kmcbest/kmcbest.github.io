/**
 * Round Badge Printer - Application Logic
 */

// Application State
let circles = Array(20).fill(null); // Stores cropped image Data URLs or null
let tempPreviewUrl = null;         // Live preview Data URL for active slot
let cropBox = { left: 0, top: 0, width: 0, height: 0 };
let dragMode = null;              // 'draw' | 'move' | 'resize' | null
let activeHandle = null;          // 'nw' | 'ne' | 'sw' | 'se' | null
let startMouseX = 0;
let startMouseY = 0;
let startCropBox = { left: 0, top: 0, width: 0, height: 0 };
let lastOverlayWidth = 0;
let zoomFactor = 1.0;              // Current image zoom factor
let fitWidth = 0;                  // Baseline fit width of the image
let fitHeight = 0;                 // Baseline fit height of the image
let isCtrlPressed = false;         // Is Photoshop Ctrl panning activated
let startScrollLeft = 0;           // Starting scrollLeft coordinate for panning
let startScrollTop = 0;            // Starting scrollTop coordinate for panning

// DOM Elements
const fileInput = document.getElementById('file-input');
const dropZone = document.getElementById('drop-zone');
const cropWorkspace = document.getElementById('crop-workspace');
const controlsCard = document.getElementById('controls-card');
const sourceImage = document.getElementById('source-image');
const cropOverlay = document.getElementById('crop-overlay');
const cropBoxEl = document.getElementById('crop-box');
const canvas = document.getElementById('crop-canvas');
const circleBoxes = document.querySelectorAll('.circle-box');
const imageWrapper = document.getElementById('image-wrapper');
const zoomSlider = document.getElementById('zoom-slider');
const zoomValue = document.getElementById('zoom-value');

const btnConfirm = document.getElementById('btn-confirm');
const btnClearAll = document.getElementById('btn-clear-all');
const btnPrint = document.getElementById('btn-print');
const btnExportPdf = document.getElementById('btn-export-pdf');
const btnExportPng = document.getElementById('btn-export-png');
const btnExportJpg = document.getElementById('btn-export-jpg');
const btnChangeImage = document.getElementById('btn-change-image');

// Initialize Scaling & Listeners
window.addEventListener('DOMContentLoaded', () => {
    initUploadListeners();
    initCropListeners();
    initControlListeners();
    initResizeObserver();
    
    // Initial scaling adjust
    adjustA4Scale();
});

// A4 Scaling Logic
function adjustA4Scale() {
    const panel = document.querySelector('.right-panel');
    const container = document.querySelector('.a4-container');
    const viewport = document.querySelector('.a4-viewport');
    if (!panel || !container || !viewport) return;
    
    const margin = 40; // padding inside right panel
    const targetW = panel.clientWidth - margin * 2;
    const targetH = panel.clientHeight - margin * 2;
    
    // Standard A4 dimensions in px at ~96 DPI
    // 210mm x 297mm -> approx 794px x 1123px
    const a4W = 794;
    const a4H = 1123;
    
    let scale = Math.min(targetW / a4W, targetH / a4H);
    
    // Constrain scale factor limits
    if (scale > 1.2) scale = 1.2;
    if (scale < 0.1) scale = 0.1;
    
    container.style.transform = `scale(${scale})`;
    viewport.style.width = `${a4W * scale}px`;
    viewport.style.height = `${a4H * scale}px`;
}

function initResizeObserver() {
    // Re-scale right-panel when container resizes
    const panel = document.querySelector('.right-panel');
    if ('ResizeObserver' in window && panel) {
        const ro = new ResizeObserver(() => {
            adjustA4Scale();
            updateOverlayBounds();
        });
        ro.observe(panel);
    } else {
        window.addEventListener('resize', () => {
            adjustA4Scale();
            updateOverlayBounds();
        });
    }
}

// Upload Handling
function initUploadListeners() {
    dropZone.addEventListener('click', () => fileInput.click());
    
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });
    
    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('dragover');
    });
    
    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        if (e.dataTransfer.files.length > 0) {
            handleImageFile(e.dataTransfer.files[0]);
        }
    });
    
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleImageFile(e.target.files[0]);
        }
    });
}

function handleImageFile(file) {
    if (!file.type.startsWith('image/')) {
        alert('请上传有效的图片文件！');
        return;
    }
    
    const reader = new FileReader();
    reader.onload = (e) => {
        sourceImage.src = e.target.result;
        sourceImage.onload = () => {
            // Setup crop elements
            dropZone.style.display = 'none';
            cropWorkspace.style.display = 'flex';
            controlsCard.style.display = 'flex';
            
            // Reset zoom controls when loading new image
            zoomFactor = 1.0;
            if (zoomSlider) {
                zoomSlider.value = 1.0;
            }
            if (zoomValue) {
                zoomValue.innerText = '1.00x';
            }
            
            // Calculate overlay bounds relative to actual image aspect ratio inside container
            lastOverlayWidth = 0; // Reset scale tracker
            updateOverlayBounds();
            adjustA4Scale();
        };
    };
    reader.readAsDataURL(file);
}

// Adjust cropping overlay size and position to match the actual displayed size of the source image
function updateOverlayBounds() {
    if (!sourceImage.complete || sourceImage.naturalWidth === 0) return;
    
    const container = document.getElementById('crop-container');
    const containerW = container.clientWidth;
    const imgW = sourceImage.naturalWidth;
    const imgH = sourceImage.naturalHeight;
    
    const imgRatio = imgW / imgH;
    
    // Always fit the image to the available width of the crop container (sidebar width)
    // This allows portrait images to extend naturally downwards and push controls below them
    const pad = 16;
    const availableW = Math.max(containerW - pad, 100);
    
    fitWidth = availableW;
    fitHeight = availableW / imgRatio;
    
    // Set actual zoomed dimensions on the wrapper
    const dispW = fitWidth * zoomFactor;
    const dispH = fitHeight * zoomFactor;
    
    imageWrapper.style.width = `${dispW}px`;
    imageWrapper.style.height = `${dispH}px`;
    
    // Scale crop selection box proportionally on resize/zoom, or setup defaults
    if (lastOverlayWidth > 0 && cropBox.width > 0) {
        const scale = dispW / lastOverlayWidth;
        cropBox.left *= scale;
        cropBox.top *= scale;
        cropBox.width *= scale;
        cropBox.height *= scale;
        
        // Boundaries checks
        cropBox.left = Math.max(0, Math.min(cropBox.left, dispW - cropBox.width));
        cropBox.top = Math.max(0, Math.min(cropBox.top, dispH - cropBox.height));
    } else {
        // Initialize default centered crop box (1:1 aspect ratio)
        const size = Math.min(dispW, dispH) * 0.6;
        cropBox = {
            left: (dispW - size) / 2,
            top: (dispH - size) / 2,
            width: size,
            height: size
        };
    }
    
    lastOverlayWidth = dispW;
    updateCropBoxDOM();
    generateCropPreview();
}

function updateCropBoxDOM() {
    cropBoxEl.style.left = `${cropBox.left}px`;
    cropBoxEl.style.top = `${cropBox.top}px`;
    cropBoxEl.style.width = `${cropBox.width}px`;
    cropBoxEl.style.height = `${cropBox.height}px`;
    cropBoxEl.style.display = 'block';
    
    // Update mask overlays positions (in CSS pixels relative to imageWrapper/cropOverlay)
    const overlayW = cropOverlay.clientWidth;
    const overlayH = cropOverlay.clientHeight;
    
    const maskTop = document.getElementById('mask-top');
    const maskBottom = document.getElementById('mask-bottom');
    const maskLeft = document.getElementById('mask-left');
    const maskRight = document.getElementById('mask-right');
    
    if (maskTop && maskBottom && maskLeft && maskRight) {
        // Top mask: from top of image to top of cropBox
        maskTop.style.top = '0px';
        maskTop.style.left = '0px';
        maskTop.style.width = `${overlayW}px`;
        maskTop.style.height = `${cropBox.top}px`;
        
        // Bottom mask: from bottom of cropBox to bottom of image
        maskBottom.style.top = `${cropBox.top + cropBox.height}px`;
        maskBottom.style.left = '0px';
        maskBottom.style.width = `${overlayW}px`;
        maskBottom.style.height = `${Math.max(0, overlayH - (cropBox.top + cropBox.height))}px`;
        
        // Left mask: fills left of cropBox (between top and bottom edges of cropBox)
        maskLeft.style.top = `${cropBox.top}px`;
        maskLeft.style.left = '0px';
        maskLeft.style.width = `${cropBox.left}px`;
        maskLeft.style.height = `${cropBox.height}px`;
        
        // Right mask: fills right of cropBox (between top and bottom edges of cropBox)
        maskRight.style.top = `${cropBox.top}px`;
        maskRight.style.left = `${cropBox.left + cropBox.width}px`;
        maskRight.style.width = `${Math.max(0, overlayW - (cropBox.left + cropBox.width))}px`;
        maskRight.style.height = `${cropBox.height}px`;
    }
}

// Cropper Interactive Event Listeners
function initCropListeners() {
    cropOverlay.addEventListener('mousedown', (e) => {
        if (!sourceImage.src) return;
        
        const overlayRect = cropOverlay.getBoundingClientRect();
        const clientX = e.clientX;
        const clientY = e.clientY;
        const x = clientX - overlayRect.left;
        const y = clientY - overlayRect.top;
        
        const target = e.target;
        
        // Snap current state
        startCropBox = { ...cropBox };
        startMouseX = clientX;
        startMouseY = clientY;
        
        if (isCtrlPressed) {
            dragMode = 'pan';
            const container = document.getElementById('crop-container');
            startScrollLeft = container.scrollLeft;
            startScrollTop = container.scrollTop;
            cropOverlay.classList.add('panning');
            cropBoxEl.classList.add('panning');
            e.preventDefault();
            return;
        }
        
        if (target.classList.contains('handle')) {
            // Resize handler clicked
            dragMode = 'resize';
            activeHandle = target.dataset.handle;
        } else if (target === cropBoxEl || cropBoxEl.contains(target)) {
            // Box dragged
            dragMode = 'move';
        } else {
            // Clicking overlay background -> Drag to draw new box
            dragMode = 'draw';
            startMouseX = x; // Store local coords relative to overlay
            startMouseY = y;
            cropBox = {
                left: x,
                top: y,
                width: 0,
                height: 0
            };
            updateCropBoxDOM();
        }
        
        e.preventDefault();
    });
    
    document.addEventListener('mousemove', (e) => {
        if (dragMode === null) return;
        
        const overlayRect = cropOverlay.getBoundingClientRect();
        const clientX = e.clientX;
        const clientY = e.clientY;
        
        // Current local position inside crop overlay
        const x = clientX - overlayRect.left;
        const y = clientY - overlayRect.top;
        
        if (dragMode === 'pan') {
            const container = document.getElementById('crop-container');
            const dx = clientX - startMouseX;
            const dy = clientY - startMouseY;
            container.scrollLeft = startScrollLeft - dx;
            container.scrollTop = startScrollTop - dy;
            return;
        }
        
        if (dragMode === 'move') {
            let dx = clientX - startMouseX;
            let dy = clientY - startMouseY;
            
            if (e.shiftKey) {
                // Dominant axis constraint (Photoshop-like Shift key behavior)
                if (Math.abs(dx) >= Math.abs(dy)) {
                    dy = 0; // Lock to horizontal movement
                } else {
                    dx = 0; // Lock to vertical movement
                }
            }
            
            let newLeft = startCropBox.left + dx;
            let newTop = startCropBox.top + dy;
            
            // Constrain inside image boundaries
            newLeft = Math.max(0, Math.min(newLeft, overlayRect.width - startCropBox.width));
            newTop = Math.max(0, Math.min(newTop, overlayRect.height - startCropBox.height));
            
            cropBox.left = newLeft;
            cropBox.top = newTop;
            
        } else if (dragMode === 'resize') {
            const dx = clientX - startMouseX;
            const dy = clientY - startMouseY;
            
            let size = startCropBox.width;
            
            switch (activeHandle) {
                case 'se': // Bottom-Right
                    size = startCropBox.width + dx;
                    // Limit bounds
                    size = Math.min(size, overlayRect.width - startCropBox.left, overlayRect.height - startCropBox.top);
                    size = Math.max(size, 20);
                    cropBox.width = size;
                    cropBox.height = size;
                    break;
                    
                case 'sw': // Bottom-Left
                    size = startCropBox.width - dx;
                    const swMaxLimit = Math.min(startCropBox.left + startCropBox.width, overlayRect.height - startCropBox.top);
                    size = Math.min(size, swMaxLimit);
                    size = Math.max(size, 20);
                    
                    cropBox.width = size;
                    cropBox.height = size;
                    cropBox.left = (startCropBox.left + startCropBox.width) - size;
                    break;
                    
                case 'ne': // Top-Right
                    size = startCropBox.width + dx;
                    const neMaxLimit = Math.min(startCropBox.top + startCropBox.height, overlayRect.width - startCropBox.left);
                    size = Math.min(size, neMaxLimit);
                    size = Math.max(size, 20);
                    
                    cropBox.width = size;
                    cropBox.height = size;
                    cropBox.top = (startCropBox.top + startCropBox.height) - size;
                    break;
                    
                case 'nw': // Top-Left
                    size = startCropBox.width - dx;
                    const nwMaxLimit = Math.min(startCropBox.left + startCropBox.width, startCropBox.top + startCropBox.height);
                    size = Math.min(size, nwMaxLimit);
                    size = Math.max(size, 20);
                    
                    cropBox.width = size;
                    cropBox.height = size;
                    cropBox.left = (startCropBox.left + startCropBox.width) - size;
                    cropBox.top = (startCropBox.top + startCropBox.height) - size;
                    break;
            }
            
        } else if (dragMode === 'draw') {
            const startX = startMouseX;
            const startY = startMouseY;
            const dx = x - startX;
            const dy = y - startY;
            
            // Constrain aspect ratio to 1:1 square
            let size = Math.min(Math.abs(dx), Math.abs(dy));
            
            if (dx >= 0 && dy >= 0) { // Drag Southeast
                const max = Math.min(overlayRect.width - startX, overlayRect.height - startY);
                size = Math.min(size, max);
                cropBox.left = startX;
                cropBox.top = startY;
            } else if (dx < 0 && dy >= 0) { // Drag Southwest
                const max = Math.min(startX, overlayRect.height - startY);
                size = Math.min(size, max);
                cropBox.left = startX - size;
                cropBox.top = startY;
            } else if (dx >= 0 && dy < 0) { // Drag Northeast
                const max = Math.min(overlayRect.width - startX, startY);
                size = Math.min(size, max);
                cropBox.left = startX;
                cropBox.top = startY - size;
            } else if (dx < 0 && dy < 0) { // Drag Northwest
                const max = Math.min(startX, startY);
                size = Math.min(size, max);
                cropBox.left = startX - size;
                cropBox.top = startY - size;
            }
            
            cropBox.width = size;
            cropBox.height = size;
        }
        
        updateCropBoxDOM();
        generateCropPreview();
    });
    
    document.addEventListener('mouseup', () => {
        if (dragMode === null) return;
        
        if (dragMode === 'pan') {
            dragMode = null;
            cropOverlay.classList.remove('panning');
            cropBoxEl.classList.remove('panning');
            return;
        }
        
        const overlayRect = cropOverlay.getBoundingClientRect();
        
        // Prevent accidental ultra-tiny box releases
        if (cropBox.width < 10) {
            const size = Math.min(overlayRect.width, overlayRect.height) * 0.6;
            cropBox = {
                left: (overlayRect.width - size) / 2,
                top: (overlayRect.height - size) / 2,
                width: size,
                height: size
            };
            updateCropBoxDOM();
            generateCropPreview();
        }
        
        dragMode = null;
        activeHandle = null;
    });
}

// Generate image crop inside hidden canvas and output as Data URL
function generateCropPreview() {
    if (!sourceImage.complete || sourceImage.naturalWidth === 0 || cropBox.width === 0) return;
    
    const scale = sourceImage.naturalWidth / cropOverlay.clientWidth;
    const srcX = cropBox.left * scale;
    const srcY = cropBox.top * scale;
    const srcSize = cropBox.width * scale;
    
    const ctx = canvas.getContext('2d');
    
    // Reset canvas to guarantee crisp transparent background support
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Draw crop onto high resolution canvas
    ctx.drawImage(
        sourceImage,
        srcX, srcY, srcSize, srcSize,
        0, 0, canvas.width, canvas.height
    );
    
    tempPreviewUrl = canvas.toDataURL('image/png');
    renderCircles();
}

// State-Driven Rendering of Circular Badge Grid
function getActiveIndex() {
    return circles.findIndex(c => c === null);
}

function renderCircles() {
    const activeIdx = getActiveIndex();
    
    circleBoxes.forEach((box, idx) => {
        const storedData = circles[idx];
        
        // Remove classes
        box.classList.remove('active', 'occupied');
        
        if (storedData) {
            // Locked Crop Image Slot
            box.classList.add('occupied');
            box.innerHTML = `<img src="${storedData}" alt="badge image">`;
        } else if (idx === activeIdx) {
            // Active Preview Slot
            box.classList.add('active');
            if (tempPreviewUrl) {
                box.innerHTML = `<img src="${tempPreviewUrl}" alt="crop preview" style="opacity: 0.82;">`;
            } else {
                box.innerHTML = `<span class="placeholder-num">${idx + 1}</span>`;
            }
        } else {
            // Empty Unoccupied Slot
            box.innerHTML = `<span class="placeholder-num">${idx + 1}</span>`;
        }
    });
    
    // Button state update
    if (activeIdx === -1) {
        btnConfirm.disabled = true;
        btnConfirm.classList.add('disabled');
        btnConfirm.innerText = "排版区已满";
    } else {
        btnConfirm.disabled = false;
        btnConfirm.classList.remove('disabled');
        btnConfirm.innerHTML = `
            <svg class="btn-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M20 6L9 17L4 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            确认裁剪 (Enter)
        `;
    }
}

// Sidebar Buttons Actions and Keyboard listeners
function initControlListeners() {
    // Confirm crop selection
    btnConfirm.addEventListener('click', () => {
        const activeIdx = getActiveIndex();
        if (activeIdx !== -1 && tempPreviewUrl) {
            // Save preview image to grid slot
            circles[activeIdx] = tempPreviewUrl;
            tempPreviewUrl = null; // Clear active workspace preview
            
            renderCircles();
            
            // Automatically regenerate preview for the next active box (duplicates position or starts fresh)
            generateCropPreview();
        }
    });
    
    // Clear all grid items
    btnClearAll.addEventListener('click', () => {
        if (confirm('确认要清空排版区所有的图片吗？此操作无法撤销。')) {
            circles = Array(20).fill(null);
            tempPreviewUrl = null;
            renderCircles();
            generateCropPreview();
        }
    });
    
    // Print layout page
    btnPrint.addEventListener('click', () => {
        window.print();
    });
    
    // Zoom Slider Input listener
    if (zoomSlider) {
        zoomSlider.addEventListener('input', (e) => {
            zoomFactor = parseFloat(e.target.value);
            if (zoomValue) {
                zoomValue.innerText = `${zoomFactor.toFixed(2)}x`;
            }
            updateOverlayBounds();
        });
    }
    
    // Right-click action to clear a locked grid item
    circleBoxes.forEach((box) => {
        box.addEventListener('contextmenu', (e) => {
            e.preventDefault();
            const idx = parseInt(box.dataset.index);
            if (circles[idx] !== null) {
                circles[idx] = null;
                // If clearing the active slot or a slot before it, reset preview
                tempPreviewUrl = null;
                renderCircles();
                generateCropPreview();
            }
        });
    });
    
    // High-DPI Export listeners
    if (btnExportPdf) {
        btnExportPdf.addEventListener('click', () => exportToPdf());
    }
    if (btnExportPng) {
        btnExportPng.addEventListener('click', () => exportToImage('png'));
    }
    if (btnExportJpg) {
        btnExportJpg.addEventListener('click', () => exportToImage('jpeg'));
    }
    
    // Change image trigger
    if (btnChangeImage) {
        btnChangeImage.addEventListener('click', () => fileInput.click());
    }
    
    // Global Keyboard Listeners
    document.addEventListener('keydown', (e) => {
        // Control key -> Activate Photoshop-like Ctrl panning
        if (e.key === 'Control') {
            isCtrlPressed = true;
            cropOverlay.classList.add('pan-ready');
            cropBoxEl.classList.add('pan-ready');
        }
        
        // Enter -> Confirm crop
        if (e.key === 'Enter') {
            const targetTag = e.target.tagName.toLowerCase();
            if (targetTag !== 'button' && targetTag !== 'input' && targetTag !== 'textarea') {
                if (!btnConfirm.disabled) {
                    btnConfirm.click();
                }
            }
        }
    });

    document.addEventListener('keyup', (e) => {
        // Control key -> Deactivate Ctrl panning
        if (e.key === 'Control') {
            isCtrlPressed = false;
            cropOverlay.classList.remove('pan-ready', 'panning');
            cropBoxEl.classList.remove('pan-ready', 'panning');
            
            if (dragMode === 'pan') {
                dragMode = null;
            }
        }
    });

    // Handle losing focus (Alt-Tab) to prevent stuck Ctrl key
    window.addEventListener('blur', () => {
        isCtrlPressed = false;
        if (cropOverlay) cropOverlay.classList.remove('pan-ready', 'panning');
        if (cropBoxEl) cropBoxEl.classList.remove('pan-ready', 'panning');
        if (dragMode === 'pan') {
            dragMode = null;
        }
    });
}

// ==========================================
// Export Helper Functions
// ==========================================

// Promisified Image Loader
function loadImage(src) {
    return new Promise((resolve) => {
        if (!src) return resolve(null);
        const img = new Image();
        img.onload = () => resolve(img);
        img.onerror = () => resolve(null);
        img.src = src;
    });
}

// Generate high resolution circular cropped image data URL (transparent corners)
function getCircularImageDataUrl(img) {
    const tempCanvas = document.createElement('canvas');
    tempCanvas.width = 1000;
    tempCanvas.height = 1000;
    const tempCtx = tempCanvas.getContext('2d');
    
    tempCtx.beginPath();
    tempCtx.arc(500, 500, 500, 0, Math.PI * 2);
    tempCtx.clip();
    tempCtx.drawImage(img, 0, 0, 1000, 1000);
    
    return tempCanvas.toDataURL('image/png');
}

// Composites the entire grid of circles onto a 300 DPI A4 canvas
async function generateHighDpiCanvas() {
    // 300 DPI A4 size: 2480px x 3508px
    const PAGE_W = 2480;
    const PAGE_H = 3508;
    const DIAMETER = 590.5; // 50mm in 300 DPI
    const MARGIN_X = 59;    // 5mm in 300 DPI
    const MARGIN_Y = 278;   // 23.5mm in 300 DPI
    
    const exportCanvas = document.createElement('canvas');
    exportCanvas.width = PAGE_W;
    exportCanvas.height = PAGE_H;
    const ctx = exportCanvas.getContext('2d');
    
    // Draw white paper background
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(0, 0, PAGE_W, PAGE_H);
    
    // Load all confirmed images
    const loadedImages = await Promise.all(circles.map(src => loadImage(src)));
    
    for (let idx = 0; idx < 20; idx++) {
        const r = Math.floor(idx / 4);
        const c = idx % 4;
        const x = MARGIN_X + c * DIAMETER;
        const y = MARGIN_Y + r * DIAMETER;
        const cx = x + DIAMETER / 2;
        const cy = y + DIAMETER / 2;
        const radius = DIAMETER / 2;
        
        const img = loadedImages[idx];
        
        if (img) {
            // Draw image clipped inside circle
            ctx.save();
            ctx.beginPath();
            ctx.arc(cx, cy, radius, 0, Math.PI * 2);
            ctx.clip();
            ctx.drawImage(img, x, y, DIAMETER, DIAMETER);
            ctx.restore();
            
            // Draw solid cutting guide line (light grey, thin)
            ctx.strokeStyle = '#a1a1aa'; // slate-400
            ctx.lineWidth = 1.5;
            ctx.beginPath();
            ctx.arc(cx, cy, radius, 0, Math.PI * 2);
            ctx.stroke();
        } else {
            // Draw dashed cutting guide line for empty space
            ctx.strokeStyle = '#d4d4d8'; // zinc-300
            ctx.lineWidth = 1.5;
            ctx.setLineDash([8, 8]);
            ctx.beginPath();
            ctx.arc(cx, cy, radius, 0, Math.PI * 2);
            ctx.stroke();
            ctx.setLineDash([]); // reset dash
        }
    }
    
    return exportCanvas;
}

// Download helper
function downloadDataUrl(dataUrl, fileName) {
    const link = document.createElement('a');
    link.download = fileName;
    link.href = dataUrl;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// Export as Image (PNG/JPEG)
async function exportToImage(format) {
    const formatName = format === 'jpeg' ? 'JPG' : 'PNG';
    const mimeType = format === 'jpeg' ? 'image/jpeg' : 'image/png';
    const fileExt = format === 'jpeg' ? 'jpg' : 'png';
    
    // Check if there is at least one image in circles
    const hasAnyImage = circles.some(c => c !== null);
    if (!hasAnyImage) {
        if (!confirm('您的排版区目前没有已确认锁定的图片，确认要导出空白模板吗？')) {
            return;
        }
    }
    
    // Change button states to loading
    const activeBtn = format === 'jpeg' ? btnExportJpg : btnExportPng;
    const originalHtml = activeBtn.innerHTML;
    activeBtn.disabled = true;
    activeBtn.innerText = `生成中...`;
    
    try {
        const canvas = await generateHighDpiCanvas();
        const dataUrl = canvas.toDataURL(mimeType, 0.95);
        downloadDataUrl(dataUrl, `徽章排版-A4-300DPI.${fileExt}`);
    } catch (err) {
        console.error('Image generation failed', err);
        alert('图片生成失败，请重试！');
    } finally {
        activeBtn.disabled = false;
        activeBtn.innerHTML = originalHtml;
    }
}

// Export as PDF
async function exportToPdf() {
    if (!window.jspdf) {
        alert('PDF 导出库加载中，或您处于离线状态。请稍候重试，或者直接使用“打印排版”并选择“保存为 PDF”。');
        return;
    }
    
    const hasAnyImage = circles.some(c => c !== null);
    if (!hasAnyImage) {
        if (!confirm('您的排版区目前没有已确认锁定的图片，确认要导出空白模板吗？')) {
            return;
        }
    }
    
    const originalHtml = btnExportPdf.innerHTML;
    btnExportPdf.disabled = true;
    btnExportPdf.innerText = `生成中...`;
    
    try {
        const { jsPDF } = window.jspdf;
        const doc = new jsPDF({
            orientation: 'portrait',
            unit: 'mm',
            format: 'a4'
        });
        
        const loadedImages = await Promise.all(circles.map(src => loadImage(src)));
        
        // Physical MM dimensions on A4
        const diameter = 50;
        const marginX = 5;
        const marginY = 23.5;
        
        for (let idx = 0; idx < 20; idx++) {
            const r = Math.floor(idx / 4);
            const c = idx % 4;
            const x = marginX + c * diameter;
            const y = marginY + r * diameter;
            
            const img = loadedImages[idx];
            
            if (img) {
                // Get transparent circle cropped PNG
                const circularDataUrl = getCircularImageDataUrl(img);
                doc.addImage(circularDataUrl, 'PNG', x, y, diameter, diameter);
                
                // Solid border
                doc.setDrawColor(161, 161, 170); // slate-400
                doc.setLineWidth(0.15); // thin cutting line
                doc.setLineDashPattern([], 0);
                doc.circle(x + 25, y + 25, 25, 'S');
            } else {
                // Dashed border for empty slots
                doc.setDrawColor(212, 212, 216); // zinc-300
                doc.setLineWidth(0.15);
                doc.setLineDashPattern([1.5, 1.5], 0);
                doc.circle(x + 25, y + 25, 25, 'S');
            }
        }
        
        doc.save('徽章排版-A4-矢量.pdf');
    } catch (err) {
        console.error('PDF generation failed', err);
        alert('PDF 生成失败，请重试！');
    } finally {
        btnExportPdf.disabled = false;
        btnExportPdf.innerHTML = originalHtml;
    }
}
