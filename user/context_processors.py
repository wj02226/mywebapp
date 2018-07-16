from .forms import LoginForm

#从django模板标签里直接引用
def login_modal_form(request):
    return {'login_modal_form': LoginForm()}