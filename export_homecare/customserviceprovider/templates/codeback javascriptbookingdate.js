$(document).ready(function() {
    var bookedDates = {{ booked_dates|safe }}.map(date => new Date(date));
    var mod1 = 1; // Initialize mod1
    var selectedDates = {}; // Object to store selected dates and their time slots

    // Function to update button state
    function updateButtonState() {
        if (mod1 === 1) {
            $('#register').attr("disabled", true).css("background", "lightblue");
        } else {
            $('#register').attr("disabled", false).css("background", "#4272d7");
        }
    }

    // Function to add selected dates to the list with time slot options
    function addSelectedDates(dates) {
        var selectedDatesList = $('#selected_dates_list');
        var list1 = $('#selected_dates_list1');
        list1.empty();
        list1.text("Selected Dates and Slots");
        selectedDatesList.empty(); // Clear the list before adding new dates

        dates.forEach(function(date, index) {
            var dateStr = date.toLocaleDateString('en-GB'); // Format date as dd-mm-yyyy
            var listItem = $('<li>').addClass('list-group-item');
            listItem.append(`<span>${dateStr}</span>`);
            var timeSlotSelect = $('<select>')
                .attr('id', 'time-slot-select-' + index) // Assign a unique id
                .addClass('form-control time-slot-select')
                .css('display', 'inline-block')
                .css('width', '150px')
                .css('margin-left', '150px');
            timeSlotSelect.append('<option value="am">AM</option>');
            timeSlotSelect.append('<option value="pm">PM</option>');
            timeSlotSelect.append('<option value="fullday">Full Day</option>');
            listItem.append(timeSlotSelect);
            selectedDatesList.append(listItem);

            // Initialize the time slot for the date if not already present
            if (!selectedDates[dateStr]) {
                selectedDates[dateStr] = 'am'; // Default value for time slot
                timeSlotSelect.val('am'); // Set default selection
            } else {
                timeSlotSelect.val(selectedDates[dateStr]); // Set previously selected value
            }
        });

        // Update hidden input with initial time slots
        updateHiddenInputs();
    }

    // Function to update hidden inputs with selected time slots
    function updateHiddenInputs() {
        // Clear existing hidden input to avoid duplication
        $("input[name='timeslot']").remove();

        var allDateTimeSlots = [];
        $('#selected_dates_list li').each(function() {
            var dateStr = $(this).find('span').text();
            var selectedTimeSlot = $(this).find('.time-slot-select').val();
            selectedDates[dateStr] = selectedTimeSlot; // Update time slot in the dictionary
            allDateTimeSlots.push( selectedTimeSlot); // Collect all date and time slot pairs
        });

        // Create a single hidden input with all date and time slot pairs
        $('<input>').attr({
            type: 'hidden',
            name: 'timeslot',
            value: allDateTimeSlots.join(',') // Concatenate all pairs with comma separator
        }).appendTo('form');
    }

    // Event handler for time slot selection change
    $(document).on('change', '.time-slot-select', function() {
        updateHiddenInputs(); // Update hidden input whenever a time slot is changed
    });

    $("#booking_dates").blur(function () {
        var n = $(this).val();

        if (n === "") { // Corrected condition to check for empty string
            mod1 = 1;
        } else {
            mod1 = 0; // Update mod1 to 0 if input is not empty
        }

        updateButtonState(); // Update button state based on mod1
    });

    // Initialize datepicker
    $('.datepicker').datepicker({
        format: 'dd-mm-yyyy',
        startDate: '0d',
        multidate: true,  // Allow multiple date selections
        todayHighlight: true,
        beforeShowDay: function(date) {
            var dateStr = date.toDateString();
            var isBooked = bookedDates.some(d => d.toDateString() === dateStr);
            var isToday = date.toDateString() === new Date().toDateString(); // Check if the date is today

            if (isBooked || isToday) {
                return {
                    enabled: false,
                    classes: 'disabled1'
                };
            }
            return;
        }
    }).on('changeDate', function(e) {
        // Enable the button when a date is selected
        if (e.dates.length > 0) {
            mod1 = 0; // Update mod1 to 0 when dates are selected
            addSelectedDates(e.dates); // Add selected dates with time slot options
        } else {
            mod1 = 1; // Update mod1 to 1 when no dates are selected
            $('#selected_dates_list').empty(); // Clear the list when no dates are selected
            selectedDates = {}; // Clear selected dates dictionary
        }
        updateButtonState(); // Update button state based on mod1
    });

    // Initially set the button state based on mod1
    updateButtonState();
});
