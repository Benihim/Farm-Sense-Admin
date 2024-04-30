
function deleteDocument(plantId){
    console.log("dOC:", plantId)
    console.log("Doc")
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/delete_document/", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            // Optionally handle response from the backend
            console.log(xhr.responseText);
        }
    };
    xhr.send(JSON.stringify({ plant_id: plantId }));
    console.log("Success")
}

function change(){
    var col = document.getElementById("doc_id");
    var id = col;
    id.textContent ="123rctfygvh45678"
    console.log("Changed")
}


    /*doc_id = document.getElementById("doc_id");
    var documentId = doc_id.textcontent;
    console.log(documentId)
    $.ajax({
        url: '/your-django-view-url/', // Replace with your Django view URL
        method: 'POST',
        document_id: documentId,
        dataType: 'json', // Specify the expected data type of the response
        success: function(response) {
            console.log('Data sent successfully:', response);
            // Optionally, update the UI or perform any other actions after successful data transmission
        },
        error: function(xhr, status, error) {
            console.error('Error sending data:', error);
        }
    });


    fetch('/delete_document/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}'
        },
        body: JSON.stringify({
            document_id: documentId
        })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message); // Show success message
        // Optionally, you can update the UI here
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred. Please try again.'); // Show error message
    });*/
    
    
