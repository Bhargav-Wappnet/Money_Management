import services.send_email as mail
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth import login, logout


def home(request):
    """
    Simpel function that render the base.html
    That show the home page of the web application.
    """
    return render(request, "base.html")


def signup(request):
    """
    A view function for signing up a new user.

    If the request method is POST, it processes the submitted form data,
    checks if the username or email already exists, creates a new user,
    generates an OTP, saves it to the database, and sends it to the user's email
    address for activation. Returns a JSON response indicating success.

    If the request method is GET, it renders the signup template.

    Args:
        request: An HttpRequest object that contains the request data.

    Returns:
        A JSON response or a rendered template.
    """
    if request.method == "POST":

        # Get form values
        username = request.POST["username"]
        email = request.POST["email"]
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        pass1 = request.POST["pass1"]

        # Check if username or email already exists
        username_exists = User.objects.filter(username=username).exists()
        email_exists = User.objects.filter(email=email).exists()

        if username_exists or email_exists:
            # Return JSON response with error message
            return JsonResponse(
                {"username_exists": username_exists, "email_exists": email_exists}
            )

        # Create user
        user = User.objects.create_user(
            username, email, pass1, first_name=fname, last_name=lname
        )
        user.is_active = False
        user.save()

        # Send activation OTP email to user
        mail.send_activation_link_email.delay(user.id)

        # Return JSON response indicating success
        return JsonResponse({"success": True})
    else:
        # Render the signup template
        return render(request, "authentication/signup.html")


def verification(request, user_id):

    # Retrieve the user object using the ID
    users = User.objects.filter(id=user_id)
    user = users.first()

    # Set the user's account to active
    user.is_active = True
    user.save()

    # Redirect the user to a success page
    return redirect('activation_success')


def activation_success(request):
    return render(request, 'activation_success.html')


def signin(request):
    """
    View for user sign in.

    If the request method is POST, it checks the entered credentials
    and returns a JSON response indicating the status of the login attempt.
    If the credentials are correct, but the user's account is not yet activated,
    the response indicates that the account is inactive and the user needs to activate it.
    If the credentials are incorrect, the response indicates that the password is incorrect.
    If the user is not found, the response indicates that the user was not found.
    If the request method is not POST, it renders the sign in page.

    :param request: The HTTP request.
    :return: The HTTP response.
    """
    if request.method == "POST":
        # Get form values
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Find user by username
        users = User.objects.filter(username=username)
        user = users.first()

        # Check if user exists and password is correct
        if user is not None:
            if user.check_password(password):
                # Check if user is activated
                if user.is_active:
                    login(request, user)
                    return JsonResponse({'success': True})
                else:
                    return JsonResponse({"notactive": True})
            else:
                return JsonResponse({"wrongpass": True})
        else:
            return JsonResponse({"usernotfound": True})

    # Render the sign in page
    return render(request, "authentication/signin.html")


def forgetpass(request):
    """
    View for handling the 'forget password' functionality.
    Sends an email to the user's email address containing a new randomly generated password.

    Returns:
        Rendered HTML template if request method is GET.
        JsonResponse with success response if request method is POST and password reset email sent successfully.
        JsonResponse with error response if request method is POST and user not found with provided email.
    """
    if request.method == "POST":
        # Get the email from the form data
        email = request.POST.get("email")

        # Check if user with given email exists
        user = User.objects.filter(email=email).first()
        if not user:
            return JsonResponse({"usernotfound": True})

        # Send forget password email.
        mail.send_forget_password_email.delay(user.id)

        # Return success response
        return JsonResponse({"success": True})

    # If request method is GET, show the forget password form
    return render(request, "forgetpass.html")


def forgetpassform(request, user_id):
    """
    View for handling the 'forget password' form.
    Renders the forgetpassform.html template for GET requests.
    Handles form submission and password reset for POST requests.
    """
    # Retrieve the user object using the ID
    users = User.objects.filter(id=user_id)
    user = users.first()

    if request.method == 'POST':
        print(request.POST)
        old_password = request.POST.get('oldpassword')
        new_password = request.POST.get('password')

        # Check if old password is correct
        if not user.check_password(old_password):
            print("asadad", old_password)
            return JsonResponse({'message': 'Invalid old password!'})

        # Set the new password and save the user object
        user.set_password(new_password)
        user.save()

        return JsonResponse({'success': True})

    return render(request, 'forgetpassform.html')


# Define the signout view
def signout(request):
    # Call the logout function with the current request object to log out the user
    logout(request)
    # Redirect the user to the signin page
    return redirect('signin')
