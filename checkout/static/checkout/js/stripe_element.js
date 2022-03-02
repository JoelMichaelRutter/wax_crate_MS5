/**
 * Below I get the stripe public key and the client secret from the html using the ID tag of the 
 * DOM element where the public key is rendered from the context.
 * I've used some jQuery to make it less verbose and i've obtained the 
 * text from the element and sliced of the first and last characters
 * to ensure that the string quotation marks are not included as this would
 * cause probles with the key's authentication and use.
 */
let stripe_public_key = $('#id_stripe_public_key').text().slice(1, -1);

let client_secret = $('#id_client_secret').text().slice(1, -1);

/**
 * Below I initiate a variable called "stripe and assign it the 
 * "Stripe" method. I pass the stripe_public_key into it. This
 * "Stripe" method is coming from the Stripe js connection implemented
 * within the base template.
 */

let stripe = Stripe(stripe_public_key);
/*I initiate a variable called elements here and drill in to the stripe
variable declared above to access the elements method.*/
let elements = stripe.elements();

// Creating a style dictionary for the card element to use when it renders.
let style = {
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
let cardElement = elements.create('card', {style, style});

/*Finally, in the below line, I mount the card into the div I've created in the checkout template
with the corresponding id.*/
cardElement.mount('#card-element');
