document.getElementById('image_file').addEventListener('change', function(e) {
    var img = document.getElementById('preview');
    var icon = this.previousElementSibling.querySelector('.bx-image-add');
    img.src = URL.createObjectURL(this.files[0]);
    img.style.display = 'block';
    icon.style.display = 'none';
});

// images required recipe.html
$(document).ready(function() {
    $('#submit-button').click(function(e) {
        if ($('#image_file').get(0).files.length === 0) {
            e.preventDefault();
            $('#file-error').show();
        }
    });
});