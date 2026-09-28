// Small progressive-enhancement helpers for PocketSmart AI.

document.addEventListener("DOMContentLoaded", () => {
  const outfitInput = document.getElementById("outfit_image");
  if (outfitInput) {
    outfitInput.addEventListener("change", () => {
      const existing = document.getElementById("outfit-preview");
      if (existing) existing.remove();

      const file = outfitInput.files[0];
      if (!file) return;

      const reader = new FileReader();
      reader.onload = (e) => {
        const img = document.createElement("img");
        img.id = "outfit-preview";
        img.className = "image-preview";
        img.src = e.target.result;
        outfitInput.parentElement.appendChild(img);
      };
      reader.readAsDataURL(file);
    });
  }
});
