document.getElementById('uploadForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    const fileInput = document.getElementById('fileInput');
    if (!fileInput.files.length) {
        alert("Please select a file.");
        return;
    }

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    const response = await fetch('/convert', {
        method: 'POST',
        body: formData,
    });

    const data = await response.json();
    if (response.ok) {
        document.getElementById('result').style.display = 'block';
        document.getElementById('downloadLink').href = `/download/${data.fileId}`;
    } else {
        alert(data.error);
    }
});
