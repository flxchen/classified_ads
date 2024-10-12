/*show cryptocurrency address*/
const cryptoTds = document.querySelectorAll('td.cryptocurrency');

// Add click event listener to each cryptocurrency <td>
cryptoTds.forEach(td => {
    td.addEventListener('click', function() {
        // Find the next sibling <td> with the class 'address'
        const addressTd = this.nextElementSibling;
        if (addressTd && addressTd.classList.contains('address')) {
            // Toggle the visibility of the address <td>
            addressTd.classList.toggle('hidden');
        }
    });
});

// Select all <td> elements with the class 'address'
const addressTds = document.querySelectorAll('td.address');

// Add click event listener to each address <td>
addressTds.forEach(td => {
  td.addEventListener('click', function() {
      // Copy the value to clipboard
      const value = this.getAttribute('data-value');
      if (navigator.clipboard) {
          navigator.clipboard.writeText(value)
              .then(() => {
                  console.log('Copied to clipboard: ' + value);
              })
              .catch(err => {
                  console.error('Could not copy text: ', err);
              });
      } else {
          // Fallback for browsers that do not support the Clipboard API
          alert('Copy this address: ' + value);
      }
  });
});