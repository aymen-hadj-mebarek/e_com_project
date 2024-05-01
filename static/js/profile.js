document.getElementById('userInfoBtn').addEventListener('click', function() {
    document.getElementById('rightSection').innerHTML = `
      <h2>User Account Information</h2>
      <p>Name: John Doe</p>
      <p>First Name: John</p>
      <p>Description: Lorem ipsum dolor sit amet</p>
      <p>Gender: Male</p>
      <p>Birth Date: 01/01/1990</p>
      <p>Phone Number: 123-456-7890</p>
      <button id="modifyInfoBtn">Modify Information</button>
    `;
    const modifyInfoBtn = document.getElementById('modifyInfoBtn');
    modifyInfoBtn.addEventListener('click', displayModal);
  });
  
  document.getElementById('orderHistoryBtn').addEventListener('click', function() {
    document.getElementById('rightSection').innerHTML = `
      <h2>Order History</h2>
      <p>Order #12345 - Date: 01/01/2024 - Status: Shipped</p>
      <p>Order #67890 - Date: 02/01/2024 - Status: Delivered</p>
    `;
  });
  
  document.getElementById('savedItemsBtn').addEventListener('click', function() {
    document.getElementById('rightSection').innerHTML = `
      <h2>Saved Items/Wishlist</h2>
      <p>Saved Item 1</p>
      <p>Saved Item 2</p>
      <p>Saved Item 3</p>
    `;
  });

  // Get the button and modal elements
const manageAccountBtn = document.getElementById('manage-account-btn');
const rightSection = document.querySelector('.right-section');
const closeModalBtn = document.getElementsByClassName('close')[0];

// Function to display the modal
function displayModal() {
  // Clear any previous content in the right section
  rightSection.innerHTML = '';

  // Create the account management form
  const accountForm = document.createElement('form');
  accountForm.id = 'account-form';
  accountForm.innerHTML = `
    <h2>Manage Account</h2>
    <!-- Add form fields for account management here -->
    <label for="name">Name:</label>
    <input type="text" id="name" name="name" required><br><br>
    <label for="firstName">First Name:</label>
    <input type="text" id="firstName" name="firstName" required><br><br>
    <label for="description">Description:</label>
    <textarea id="description" name="description" rows="4" required></textarea><br><br>
    <label for="gender">Gender:</label>
    <input type="text" id="gender" name="gender" required><br><br>
    <label for="birthdate">Birth Date:</label>
    <input type="date" id="birthdate" name="birthdate" required><br><br>
    <label for="phoneNumber">Phone Number:</label>
    <input type="tel" id="phoneNumber" name="phoneNumber" required><br><br>
    <!-- Submit button -->
    <input type="submit" value="Save Changes">
  `;

  // Append the form to the right section
  rightSection.appendChild(accountForm);

  // Display the right section
  rightSection.style.display = 'block';
}

// Function to close the modal
function closeModal() {
  // Hide the right section
  rightSection.style.display = 'none';
}

// Event listener for opening the modal
manageAccountBtn.addEventListener('click', displayModal);



// Event listener for closing the modal when the close button is clicked
closeModalBtn.addEventListener('click', closeModal);

// Event listener for closing the modal when clicking outside of it
window.addEventListener('click', (event) => {
  if (event.target == rightSection) {
    closeModal();
  }
});

// Function to handle form submission
document.getElementById('account-form').addEventListener('submit', (event) => {
  event.preventDefault(); // Prevent default form submission

  // Get form data
  const formData = new FormData(event.target);

  // You can now handle the form data, such as sending it to a server for processing
  // For demonstration purposes, let's log the form data to the console
  for (const pair of formData.entries()) {
    console.log(`${pair[0]}: ${pair[1]}`);
  }

  // Close the modal after saving changes
  closeModal();
});
