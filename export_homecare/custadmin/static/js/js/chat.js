const chatBox = document.querySelector('.chat-box');
const noMessageText = document.querySelector('.no-message');

// Example function to add a message
function addMessage(message) {
  const messageElement = document.createElement('div');
  messageElement.textContent = message;
  chatBox.appendChild(messageElement);

  // Hide no message text if a message is added
  noMessageText.style.display = 'none';
}

// Example usage
// Uncomment below to simulate adding a message
// addMessage("Hello, this is a test message.");
