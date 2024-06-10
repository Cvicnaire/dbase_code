$(document).ready(function() {
   
    // function to fetch html content
    function loadContent(url) {
        fetch(url)
            .then(response => response.text())
            .then(html => {
                document.getElementById('content').innerHTML = html;
            })
            .catch(error => console.error('Error fetching content:', error));
    }

    // Function to handle collapsible elements
    $('.collapsible').click(function() {
        $(this).toggleClass("active");
        var content = $(this).next();
        if (content.css('display') === "block") {
            content.css('display', 'none');
        } else {
            content.css('display', 'block');
        }
    });
 

    // Event listeners for subset buttons
    $('.subset-button').click(function(e) {
        e.preventDefault();
        var targetId = $(this).attr('data-target'); // Get the target id from data attribute
        // Hide all form sections
        $('.form-section').addClass('hidden');
        // Show the corresponding form section
        $('#' + targetId).removeClass('hidden');
        // Load form content based on selected form
        $('#' + targetId).load(targetId + '_form.html');
    });
    // Function to populate the table

    // Function to set color based on date proximity
    function setColorBasedOnDate(dateString, cell) {
        if (!dateString) {
            return; // Skip null or empty date strings
        }

        // Parse the date string in 'YYYY-MM-DD' format
        var parts = dateString.split('-');
        var year = parseInt(parts[0]);
        var month = parseInt(parts[1]) - 1; // Months are 0-based in JavaScript
        var day = parseInt(parts[2]);
        var date = new Date(year, month, day);
        var today = new Date();

        // Calculate the difference in days between the dates
        var differenceInDays = Math.floor((date - today) / (1000 * 60 * 60 * 24));

        // Set color based on proximity
        if (differenceInDays <= 0) {
            cell.css('backgroundColor', 'red').css('color', 'white'); // Past or today's date
        } else if (differenceInDays <= 7) {
            cell.css('backgroundColor', 'orange'); // Within a week
        }
        // You can add more conditions for different proximity ranges if needed
    }

    function populateTable(selector) {
        $('#main').empty();
    
        $.ajax({
            url: 'https://bioed.bu.edu/cgi-bin/students_24/Team_4/tables.py',
            method: 'POST',
            data: { selector: selector },
            success: function(response) {
                // Log the selector value to debug
                console.log('Selector:', selector);
                console.log('Received response:', response);
                var result = JSON.parse(response);
                var fieldNames = result.fields;
                var dataArray = result.data;
                var title = '';
    
                // Set title based on the selector
                if (selector === 'master') {
                    title = 'Active Mosquito Lines';
                } else if (selector === 'passage') {
                    title = 'Passage Timeline';
                } else if (selector === 'retired') {
                    title = 'Retired Lines';
                } else if (selector === 'simple_passage') {
                    title = 'Passage Records';
                } else if (selector === 'simple_clutch') {
                    title = 'Clutch Records';
                } else if (selector === 'simple_sort') {
                    title = 'Sorting Records';
                }
    
                if (dataArray.length === 0) {
                    $('#main').addClass('error').text("Mosquito line tables not found");
                } else {
                    $('#main').removeClass('error');
                    // Create title element
                    var titleElement = $('<h4>').text(title).addClass('custom-title');
                    $('#main').append(titleElement);
    
                    // Count the number of records
                    var recordCount = dataArray.length;
                    var countMessage = 'There are a total of ' + recordCount + ' records.';
                    var countElement = $('<h5>').text(countMessage);
                    $('#main').append(countElement);
    
                    // Create the DataTable structure
                    var dataTable = $('<table>').attr('id', 'myTable').addClass('display');
                    var thead = $('<thead>');
                    var headerRow = $('<tr>').addClass('custom-table-header');
    
                    // Create table headers with center alignment
                    fieldNames.forEach(function(fieldName) {
                        var th = $('<th>').text(fieldName).css('text-align', 'center');
                        headerRow.append(th);
                    });
                    thead.append(headerRow);
                    dataTable.append(thead);
    
                    // Create table body
                    var tbody = $('<tbody>');
                    dataArray.forEach(function(entry) {
                        var row = $('<tr>').addClass('custom-table-row');
                        for (var key in entry) {
                            var cell = $('<td>').text(entry[key]);
                            row.append(cell);

                            // Check if the cell belongs to "Next Passage" column
                            if (fieldNames[key] === 'Next Passage') {
                                setColorBasedOnDate(entry[key], cell);
                            }
    
                            // Dynamically adjust column width based on content length
                            var contentWidth = getTextWidth(entry[key]);
                            var currentWidth = cell.width();
                            if (contentWidth > currentWidth) {
                                cell.width(contentWidth);
                            }
                        }
                        tbody.append(row);
                    });
                    dataTable.append(tbody);
    
                    // Append the DataTable to the main div
                    $('#main').append(dataTable);
    
                    // Initialize the DataTable
                    $('#myTable').DataTable({
                        // "pageLength": 100
                        "paging": false
                    });
    
                    // Add the Excel download button
                    var downloadButton = $('<button>').attr('id', 'download_csv_btn').text('Download CSV');
                    $('#main').append(downloadButton);
    
                    // Bind click event to the download button
                    $('#download_csv_btn').click(function() {
                        downloadExcel(dataArray, title); // Function to download Excel
                    });
                }
            },
            error: function(xhr, status, error) {
                console.error(error);
            }
        });
    }
    

    // Function to get text width for adjusting column width
    function getTextWidth(text) {
        var element = $('<span>').text(text).css({ 'white-space': 'nowrap', 'visibility': 'hidden' });
        $('body').append(element);
        var width = element.width();
        element.remove();
        return width;
    }
    
      

    // Bind event listener to the form submission
    $('#table_form').submit(function(event) {
        event.preventDefault(); // Prevent default form submission
        var selector = $('#table_selector').val(); // Get the selected table view
        populateTable(selector); // Populate the table based on the selected value
    });

    function downloadExcel(dataArray, title) {
        // Convert JSON data to CSV format
        var csvContent = 'data:text/csv;charset=utf-8,';
    
        // Add headers
        var headers = Object.keys(dataArray[0]);
        csvContent += headers.join(',') + '\n';
    
        // Add rows
        dataArray.forEach(function(entry) {
            var row = [];
            headers.forEach(function(header) {
                row.push(entry[header]);
            });
            csvContent += row.join(',') + '\n';
        });
    
        // Get today's date
        var today = new Date();
        var dd = String(today.getDate()).padStart(2, '0');
        var mm = String(today.getMonth() + 1).padStart(2, '0'); // January is 0!
        var yyyy = today.getFullYear();
        today = mm + '-' + dd + '-' + yyyy;
    
        // Create Blob object
        var blob = new Blob([csvContent], { type: 'text/csv' });
    
        // Create download link
        var downloadLink = document.createElement('a');
        downloadLink.href = window.URL.createObjectURL(blob);
        downloadLink.setAttribute('download', title + '_' + today + '.csv');
    
        // Append download link to DOM
        document.body.appendChild(downloadLink);
    
        // Trigger click event on download link
        downloadLink.click();
    
        // Remove download link from DOM
        document.body.removeChild(downloadLink);
    }
    
  // Fetch the header HTML file and insert it into the placeholder div
  fetch('header.html')
  .then(response => response.text())
  .then(html => {
      document.getElementById('header-placeholder').innerHTML = html;
  })
  .catch(error => {
      console.error('Error fetching header:', error);
  });
});

// Close popup when "Close" button is clicked
$('#closePopupButton').click(function() {
    $('#popupForm').hide();
    resetForm(); // Reset form and hide completion message
});
// Show popup when "Add New User" button is clicked
$('#addUserButton').click(function() {
    $('#popupForm').show();
    resetForm(); // Reset form and hide completion message
});
// Close popup when clicking outside the form
$(document).mouseup(function(e) {
    var popup = $('#popupForm');
    if (!popup.is(e.target) && popup.has(e.target).length === 0) {
        popup.hide();
        resetForm(); // Reset form and hide completion message
    }
});


// List Population    \

// Populate Role dropdown menu using AJAX
    //   $.ajax({
    //     url: 'https://bioed.bu.edu/cgi-bin/students_24/Team_4/dropdowns.py',
    //     method: 'GET',
    //     dataType: 'json',
    //     data: {'selector': 'lab_role_dropdown'},
    //     success: function(data) {
    //         populate_list("#lab_role", data);
    //     },
    //     error: function(xhr, status, error) {
    //         console.error('Error fetching data:', error);
    //         // Handle error, such as showing a default value or retrying
    //     }
    //   });