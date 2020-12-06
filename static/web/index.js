const form = $('#contact-form');
const fieldset = form.children('fieldset');
const alert = $('#alert');

function setLoading(isLoading) {
    if (isLoading) {
        fieldset.attr('disabled', true);
    } else {
        fieldset.removeAttr('disabled');
    }
}

function showAlert(isVisible, isSuccess) {
    if (isVisible) {
        const message = isSuccess ? 'Email successfully sent.' : '<b>Error!</b> Failed to send the email. Try later.';
        alert.html(message).attr('class', `alert alert-${isSuccess ? 'success' : 'danger'}`);
    } else {
        alert.attr('class', 'd-none');
    }
}

function sendEmail(data) {
    return new Promise((resolve, reject) => {
        $.ajax({
            type: 'POST',
            url: '/api/send-email',
            data,
            success: resolve,
            error: reject,
            dataType: 'application/json'
        });
    });
}

form.submit(async function (event) {
    event.preventDefault();
    setLoading(true);
    showAlert(false)
    const body = {
        csrfmiddlewaretoken: this.csrfmiddlewaretoken.value,
        name: this.name.value,
        email: this.email.value,
        subject: this.subject.value,
        message: this.message.value,
    }
    try {
        await sendEmail(body);
        showAlert(true, true);
        form[0].reset();
    } catch (e) {
        console.error(e);
        showAlert(true, false);
    }
    setLoading(false);
});
