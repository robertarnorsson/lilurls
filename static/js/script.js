const defaultIcon = document.getElementById('default-icon');
const successIcon = document.getElementById('success-icon');

const copyToClipboard = (text) => {
  navigator.clipboard.writeText(text);

  showSuccess();

  setTimeout(() => {
    resetToDefault();
  }, 2000);
}

const showSuccess = () => {
    defaultIcon.classList.add('hidden');
    successIcon.classList.remove('hidden'); 
}

const resetToDefault = () => {
    defaultIcon.classList.remove('hidden');
    successIcon.classList.add('hidden');
}
