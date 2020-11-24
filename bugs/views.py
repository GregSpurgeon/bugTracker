from django.shortcuts import render, reverse, HttpResponseRedirect, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from bugs.forms import LoginForm, TicketForm
from bugs.models import Ticket, MyUser

# Create your views here.


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request,
                                username=data['username'],
                                password=data['password'])
            if user:
                login(request, user)
                return HttpResponseRedirect(
                    request.GET.get('next',
                                    reverse('home')))
    form = LoginForm()
    return render(request, 'login_form.html', {"form": form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


def index_view(request):
    home = "index.html"
    ticket_new = Ticket.objects.filter(ticket_status_choice="New")
    ticket_inprogress = Ticket.objects.filter(ticket_status_choice="In Progress")
    ticket_done = Ticket.objects.filter(ticket_status_choice="Done")
    ticket_invalid = Ticket.objects.filter(ticket_status_choice="Invalid")
    return render(request, home, {'ticket_new': ticket_new,
                                  "ticket_inprogress": ticket_inprogress,
                                  'ticket_done': ticket_done,
                                  'ticket_invalid': ticket_invalid})


def create_ticket_view(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Ticket.objects.create(
              title=data['title'],
              description=data['description'],
              user_who_filed=request.user,
              ticket_status_choice="New"
            )
            return redirect("/")
    form = TicketForm()
    return render(request, "create_ticket_form.html", {'form': form})


def edit_ticket_view(request, pk=None):
    instance = get_object_or_404(Ticket, pk=pk)
    if request.method == 'POST':
        form = TicketForm(request.POST, instance=instance)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.save()
            return redirect('/')
    form = TicketForm(instance=instance)
    return render(request, 'create_ticket_form.html', {"form": form})


def ticket_done_view(request, ticket_id):
    ticket = Ticket.objects.filter(id=ticket_id).first()
    ticket.ticket_status_choice = "Done"
    ticket.assigned_user_ticket = None
    ticket.user_who_completed = request.user
    ticket.save()
    return HttpResponseRedirect(reverse('ticket_page',
                                        kwargs={'ticket_id': ticket.id}))


def ticket_new_view(request, ticket_id):
    ticket = Ticket.objects.filter(id=ticket_id).first()
    ticket.ticket_status_choice = "New"
    ticket.assigned_user_ticket = None
    ticket.user_who_completed = None
    ticket.save()
    return HttpResponseRedirect(reverse('ticket_page',
                                        kwargs={'ticket_id': ticket.id}))


def assign_ticket_view(request, ticket_id):
    ticket = Ticket.objects.filter(id=ticket_id).first()
    ticket.ticket_status_choice = "In Progress"
    ticket.assigned_user_ticket = request.user
    ticket.user_who_completed = None
    ticket.save()
    return HttpResponseRedirect(reverse('ticket_page',
                                        kwargs={'ticket_id': ticket.id}))


def ticket_invalid_view(request, ticket_id):
    ticket = Ticket.objects.filter(id=ticket_id).first()
    ticket.ticket_status_choice = "Invalid"
    ticket.user_who_completed = None
    ticket.assigned_user_ticket = None
    ticket.save()
    return HttpResponseRedirect(reverse('ticket_page',
                                        kwargs={'ticket_id': ticket.id}))


def ticket_detail_view(request, ticket_id):
    current_ticket = Ticket.objects.get(id=ticket_id)
    return render(request, 'ticket_detail.html', {'ticket': current_ticket})


def myuser_detail_view(request, myuser_id):
    myuser = MyUser.objects.filter(id=myuser_id).first()
    ticket_filed = Ticket.objects.filter(user_who_filed=myuser_id)
    ticket_assigned = Ticket.objects.filter(assigned_user_ticket=myuser_id)
    ticket_completed = Ticket.objects.filter(user_who_completed=myuser_id)
    return render(request, 'user_detail.html', {"myuser": myuser,
                                                "tickets": ticket_filed,
                                                "tickets1": ticket_assigned,
                                                "tickets2": ticket_completed})
