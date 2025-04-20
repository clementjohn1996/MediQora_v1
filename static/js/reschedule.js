// reschedule.js

// Open the modal and set entity type and ID
function openRescheduleModal(entityType, entityId) {
    document.getElementById('entity_id').value = entityId;
    document.getElementById('entity_type').value = entityType;
    // Show the modal
    $('#rescheduleModal').modal('show');
}

// Restrict date selection to not allow past dates
const today = new Date().toISOString().split('T')[0];
document.getElementById('scheduled_date').setAttribute('min', today);

// Handle form submission
document.getElementById('rescheduleForm').onsubmit = function(event) {
    event.preventDefault();

    const entityId = document.getElementById('entity_id').value;
    const entityType = document.getElementById('entity_type').value;
    const scheduledDate = document.getElementById('scheduled_date').value;

    // Make an AJAX request to reschedule
    $.ajax({
        url: `/enquiry/reschedule/${entityType}/${entityId}/`,
        method: 'POST',
        data: {
            'scheduled_date': scheduledDate,
            'csrfmiddlewaretoken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        success: function(response) {
            if (response.status === 'success') {
                alert('Rescheduled successfully');
                location.reload(); // Reload page to reflect changes
            } else {
                alert('Error rescheduling. Please try again.');
            }
        },
        error: function() {
            alert('Error occurred while rescheduling.');
        }
    });
};
