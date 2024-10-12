document.addEventListener("DOMContentLoaded", function () {
  const navLinks = document.querySelectorAll(".nav-link[data-section]");
  const sections = document.querySelectorAll("main > section");

  function showSection(sectionId) {
    sections.forEach((section) => {
      if (section.id === sectionId) {
        section.classList.remove("hidden");
      } else {
        section.classList.add("hidden");
      }
    });
  }

  navLinks.forEach((link) => {
    link.addEventListener("click", function (e) {
      e.preventDefault();
      const sectionId = this.getAttribute("data-section");
      showSection(sectionId);

      // Update active state
      navLinks.forEach((l) => l.classList.remove("active"));
      this.classList.add("active");

      // If switching to account settings, ensure the active tab content is shown
      if (sectionId === "account-settings") {
        const activeTab = document.querySelector("#myTab button.active");
        if (activeTab) {
          const tabContent = document.querySelector(
            activeTab.getAttribute("data-bs-target")
          );
          if (tabContent) {
            tabContent.classList.add("show", "active");
          }
        }
      }
      
    });
  });

  // Show account settings by default
  showSection("account-settings");
});
