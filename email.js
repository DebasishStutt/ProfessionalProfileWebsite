const EMAIL_ADDRESS = "debasishformasters@gmail.com";

const copyButton = document.querySelector("[data-copy-email]");

const setButtonLabel = (label) => {
  if (copyButton) {
    copyButton.textContent = label;
  }
};

const fallbackCopy = () => {
  const input = document.createElement("input");
  input.value = EMAIL_ADDRESS;
  document.body.appendChild(input);
  input.select();
  const successful = document.execCommand("copy");
  document.body.removeChild(input);
  return successful;
};

if (copyButton) {
  copyButton.addEventListener("click", async () => {
    try {
      if (navigator.clipboard && window.isSecureContext) {
        await navigator.clipboard.writeText(EMAIL_ADDRESS);
        setButtonLabel("Copied!");
      } else if (fallbackCopy()) {
        setButtonLabel("Copied!");
      } else {
        setButtonLabel("Copy failed");
      }
    } catch (error) {
      setButtonLabel("Copy failed");
    }

    setTimeout(() => setButtonLabel("Copy Email Address"), 1800);
  });
}
