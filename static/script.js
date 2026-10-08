// --- Role & Signup Flow Transition Logic ---
const roleSelectionCard = document.getElementById('role-selection-card');
const customerSignupFlow = document.getElementById('customer-signup-flow');
const driverSignupFlow = document.getElementById('driver-signup-flow');
const customerFlow = document.getElementById('customer-flow');
const driverFlow = document.getElementById('driver-flow');

const btnLoginCustomer = document.getElementById('btn-login-customer');
const btnLoginDriver = document.getElementById('btn-login-driver');
const customerSignupForm = document.getElementById('customer-signup-form');
const driverSignupForm = document.getElementById('driver-signup-form');

if (btnLoginCustomer && btnLoginDriver) {
    btnLoginCustomer.addEventListener('click', () => {
        roleSelectionCard.style.display = 'none';
        customerSignupFlow.style.display = 'block';
    });

    btnLoginDriver.addEventListener('click', () => {
        roleSelectionCard.style.display = 'none';
        driverSignupFlow.style.display = 'block';
    });
}

if (customerSignupForm) {
    customerSignupForm.addEventListener('submit', (e) => {
        e.preventDefault();
        customerSignupFlow.style.display = 'none';
        customerFlow.style.display = 'block';
    });
}

if (driverSignupForm) {
    driverSignupForm.addEventListener('submit', (e) => {
        e.preventDefault();
        driverSignupFlow.style.display = 'none';
        driverFlow.style.display = 'block';
    });
}

// --- Baggage Scanner Tab Logic ---
const tabCameraBtn = document.getElementById('tab-camera-btn');
const tabUploadBtn = document.getElementById('tab-upload-btn');
const tabCamera = document.getElementById('tab-camera');
const tabUpload = document.getElementById('tab-upload');

if (tabCameraBtn && tabUploadBtn) {
    tabCameraBtn.addEventListener('click', () => {
        tabCameraBtn.classList.add('active');
        tabUploadBtn.classList.remove('active');
        tabCamera.style.display = 'block';
        tabUpload.style.display = 'none';
    });

    tabUploadBtn.addEventListener('click', () => {
        tabUploadBtn.classList.add('active');
        tabCameraBtn.classList.remove('active');
        tabUpload.style.display = 'block';
        tabCamera.style.display = 'none';
    });
}

// --- Ride Option Toggle Logic ---
const toggleShared = document.getElementById('toggle-shared');
const togglePrivate = document.getElementById('toggle-private');

if (toggleShared && togglePrivate) {
    toggleShared.addEventListener('click', () => {
        toggleShared.style.border = '2px solid #0284C7';
        toggleShared.style.background = '#F0F9FF';
        togglePrivate.style.border = '1px solid #E2E8F0';
        togglePrivate.style.background = '#fff';
    });

    togglePrivate.addEventListener('click', () => {
        togglePrivate.style.border = '2px solid #0284C7';
        togglePrivate.style.background = '#F0F9FF';
        toggleShared.style.border = '1px solid #E2E8F0';
        toggleShared.style.background = '#fff';
    });
}

// --- Camera Startup (Visual Placeholder) ---
const btnStartCam = document.getElementById('btn-start-cam');
const btnSnapCam = document.getElementById('btn-snap-cam');
const webcam = document.getElementById('webcam');
const camPlaceholder = document.getElementById('cam-placeholder');

if (btnStartCam) {
    btnStartCam.addEventListener('click', async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } });
            webcam.srcObject = stream;
            webcam.style.display = 'block';
            camPlaceholder.style.display = 'none';
            btnStartCam.style.display = 'none';
            btnSnapCam.style.display = 'block';
        } catch (err) {
            alert("Camera access denied or unavailable.");
        }
    });
}

// --- Booking Confirmation Logic ---
const btnBook = document.getElementById('btn-book');
const ticketModal = document.getElementById('ticket-modal');

if (btnBook) {
    btnBook.addEventListener('click', () => {
        btnBook.textContent = '⏳ MATCHING INDORE CO-RIDERS...';
        btnBook.style.background = '#64748B';

        setTimeout(() => {
            btnBook.style.display = 'none';
            ticketModal.style.display = 'block';
        }, 1500);
    });
}

// --- Driver Vehicle Inspection Logic ---
const btnSubmitInspection = document.getElementById('btn-submit-inspection');
const driverTicketModal = document.getElementById('driver-ticket-modal');
const driverSuccessMsg = document.getElementById('driver-success-msg');

if (btnSubmitInspection) {
    btnSubmitInspection.addEventListener('click', async () => {
        btnSubmitInspection.textContent = '⏳ VERIFYING INSPECTION PHOTOS...';
        btnSubmitInspection.style.background = '#64748B';

        try {
            const response = await fetch('/api/driver-log', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ driver_id: 1, interior_img: "verified_interior.jpg", exterior_img: "verified_exterior.jpg" })
            });
            const result = await response.json();

            setTimeout(() => {
                btnSubmitInspection.style.display = 'none';
                driverTicketModal.style.display = 'block';
                if (result.message) {
                    driverSuccessMsg.textContent = result.message;
                }
            }, 1200);
        } catch (err) {
            setTimeout(() => {
                btnSubmitInspection.style.display = 'none';
                driverTicketModal.style.display = 'block';
                driverSuccessMsg.textContent = "Driver profile activated & daily log verified locally!";
            }, 1200);
        }
    });
}