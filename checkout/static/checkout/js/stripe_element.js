/**
 * Below I get the stripe public key and the client secret from the html using the ID tag of the 
 * DOM element where the public key is rendered from the context.
 * I've used some jQuery to make it less verbose and i've obtained the 
 * text from the element and sliced of the first and last characters
 * to ensure that the string quotation marks are not included as this would
 * cause probles with the key's authentication and use.
 */
var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);

var clientSecret = $('#id_client_secret').text().slice(1, -1);

/**
 * Below I initiate a variable called "stripe and assign it the 
 * "Stripe" method. I pass the stripe_public_key into it. This
 * "Stripe" method is coming from the Stripe js connection implemented
 * within the base template.
 */

var stripe = Stripe(stripePublicKey);
/*I initiate a variable called elements here and drill in to the stripe
variable declared above to access the elements method.*/
var elements = stripe.elements();

// Creating a style dictionary for the card element to use when it renders.
var style = {
    base: {
        fontFamily: "'Roboto-Mono', monospace",
        fontSize: "18px",
    },
    invalid: {
        color: '#a13b2c',
        iconColor: '#a13b2c'
    }
};

/*Below I initiate a new variable "cardElement" and use the elements variable
to drill into the previously declared elements variable and create a new card element.
I also pass it the style dictionary created above to ensure that the type setting
and font size are consistent with the rest of the form.*/
var cardElement = elements.create('card', {style, style});

/*Finally, in the below line, I mount the card into the div I've created in the checkout template
with the corresponding id.*/
cardElement.mount('#card-element');

/**
 * In the below code block, I populate the card-errors div. Firstly, I'ved added an event listener to the 
 * card element. I've declared the varaible errorContainer and assigned it a value of the DOM element "card-errors"
 * It listens for a change within the element and everytime the card element is changed
 * it listens for an event. If the event is an error, the conditional check decares a 
 * variable called "content" which I initilaise to some HTML containing a template literal.
 * Within the html, I create two spans with an icon and then another span which then drills via dot notation
 * into the event paramenter then into the error and then arriving at the message.
 * I then assign the content variable outside the template literal to the errorContainer via the "html" jquery method.
 */
cardElement.addEventListener('change', function(event) {
    var errorContainer = document.getElementById('card-errors');
    if (event.error) {
        var content = `
            <span class="icon wax-crate-red-font ps-1" role="alert">
                <i class="fa-solid fa-circle-exclamation"></i>
            </span>
            <span class="wax-crate-red-font ps-1">${event.error.message}</span>
        `;
        $(errorContainer).html(content);
    } else {
        errorContainer.textContent = '';
    }
});


// The below code handles the submission of the checkout form.

// Firsty, I've accessed the form from the DOM with the id "checkout-form with abit of jQuery"
var checkoutForm = document.getElementById('checkout-form');

/* Add an event listener to the form to listen for the submit event.
When the submit event is triggered, the function within the event listener is
excecuted.*/
checkoutForm.addEventListener('submit', function(ev) {
    /* Firstly, prevent the form from posting data to ensure that 
    so that we can complete the relevant error checks */
    ev.preventDefault();
    /* In this part of the script, I disable the card element and submit
    button by using the update function and passing it an object with a key 
    value pair of 'disabled': true. To access the submit button, I call the DOM
    element using jQuery and set the disabled attribute on the element to true.*/
    cardElement.update({'disabled': true});
    $('checkout-submit').attr('disabled', true);
    $('#checkout-form').fadeToggle(100);
    $('#form-loading').fadeToggle(100);
    /* Usinng the stripe confirm card payment method, I pass in the
    client secret decalred at the top of the script which accesses
    the key which is inserted into the template from the view which
    in turn accesses it from the settings which is passed through the 
    environmnent from env.py 

    This an async function so I provide the card to stripe and in the 
    "then" block I wait for the result of the interaction. Once the 
    result is returned, I pass it in to the then block to check what
    result is returned from stripe.
    */
    stripe.confirmCardPayment(clientSecret, {
        payment_method: {
            card: cardElement,
        }
    }).then(function(result) {
        if (result.error) {
            /* Similar to the logic above, if the result is an error I populate
            the error div with the message that is returned */
            var errorContainer = document.getElementById('card-errors');
            var content = `
                <span class="icon wax-crate-red-font ps-1" role="alert">
                    <i class="fa-solid fa-circle-exclamation"></i>
                </span>
                <span class="wax-crate-red-font ps-1">${result.error.message}</span>
            `;
            $(errorContainer).html(content);
            $('#checkout-form').fadeToggle(100);
            $('#form-loading').fadeToggle(100);
            // If there has been an error, I re-enable the card element and from submit button.
            cardElement.update({'disabled': false});
            $('checkout-submit').attr('disabled', false);
        /* In this else block, I handle the successsful submission to stripe
        by submitting the payment details to stripe provided that the result
        status is equal to 'succeeded' */
        } else {
            if (result.paymentIntent.status === 'succeeded') {
                checkoutForm.submit();
            }
        };
    });
});



