document.addEventListener("DOMContentLoaded", function () {
    const sidebar = document.getElementById("sidebar");
    const toggleBtn = document.getElementById("sidebarToggle");
    const minimizeBtn = document.getElementById("sidebarMinimize");
    const minimizeIcon = minimizeBtn?.querySelector("i");
    const spans = sidebar.querySelectorAll(".menu-text");

    // Carregar estado salvo do localStorage
    const savedState = localStorage.getItem("sidebarMinimized");

    if (window.innerWidth >= 992) { // Desktop
        if (document.documentElement.classList.contains("sidebar-minimized")) {
            sidebar.classList.add("minimized");
            spans.forEach(span => span.style.display = "none");
            minimizeIcon?.classList.replace("bi-chevron-double-left", "bi-chevron-double-right");
        } else {
            sidebar.classList.remove("minimized");
            spans.forEach(span => span.style.display = "inline");
            minimizeIcon?.classList.replace("bi-chevron-double-right", "bi-chevron-double-left");
        }
    }

    function toggleSidebarMinimize() {
        const isMinimized = sidebar.classList.toggle("minimized");
        localStorage.setItem("sidebarMinimized", isMinimized); // salva o estado

        if (isMinimized) {
            minimizeIcon?.classList.replace("bi-chevron-double-left", "bi-chevron-double-right");
            spans.forEach(span => span.style.display = "none");
        } else {
            minimizeIcon?.classList.replace("bi-chevron-double-right", "bi-chevron-double-left");
            spans.forEach(span => span.style.display = "inline");
        }
    }

    function toggleSidebarMobile() {
        sidebar.classList.toggle("show");
    }

    // Eventos
    toggleBtn?.addEventListener("click", toggleSidebarMobile);
    minimizeBtn?.addEventListener("click", toggleSidebarMinimize);
});