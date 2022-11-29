from django.shortcuts import render,redirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from .models import Event, Venue
from .forms import VenueForm,EventForm
from django.http import HttpResponseRedirect
from django.http import HttpResponse
import csv
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
#import pagination staff
from django.core.paginator import Paginator

#generate pdf file
def venue_pdf(request):
    #create bytestream buffer
    buf = io.BytesIO()
    #create canvas
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
#create text objects
    textob= c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)
#Designate models
    venues = Venue.objects.all()
#create blank list
    lines = []
    #loop thu the venues
    for venue in venues:
        lines.append(venue.name)
        lines.append(venue.address)
        lines.append(venue.zip_code)
        lines.append(venue.phone)
        lines.append(venue.web)
        lines.append(venue.email_address)
        lines.append("================================")
        

    #finish up
        
    for line in lines:
        textob.textLine(line)
        #finish up
        c.drawText(textob)
        c.showPage()
        c.save()
        buf.seek(0)

        #return something
    return FileResponse(buf, as_attachment=True, filename ='venue.pdf')

def venue_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition']= 'attachment; filename=venues.csv'

    #create csv writter
    writer = csv.writer(response)
    
    #Designate the model
    venues = Venue.objects.all()

    #dd column headings to the csv files
    writer.writerow(['Venue Name', 'Address', 'zip code', 'phone', 'web Address', 'email_address'])

    #loop tru the uput
    for venue in venues:
        writer.writerow([venue.name,venue.address,venue.zip_code,venue.phone,venue.web, venue.email_address])
    
    return response

#Generate text file
def venue_text(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition']= 'attachment; filename=venues.txt'

    #Designate the model
    venues = Venue.objects.all()

    lines = []
    for venue in venues:
        lines.append(f'{venue.name}\n{venue.address}\n{venue.zip_code}\n{venue.phone}\n{venue.web}\n\n')
    #write to a Textfile
    response.writelines(lines)
    return response

# delete event here.
def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    event.delete()
    return redirect('all-events')
#delete venue
def delete_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue.delete()
    return redirect('list-venues')
#update event
def update_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    form = EventForm(request.POST or None, instance=event)
    if form.is_valid():
        form.save()
        return redirect('all-events')

    return render(request, 'events/update_event.html', 
       {'Event':event, 
       'form':form } 
    )

#add event
def add_event(request):
    submitted = False
    if request.method =="POST":
        form = EventForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('add_event?submitted = True')
    else:
        form = EventForm
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'events/add_event.html', {'form':form, 'submitted':submitted})

#update venue
def update_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    form = VenueForm(request.POST or None, instance=venue)
    if form.is_valid():
        form.save()
        return redirect('list-venues')

    return render(request, 'events/update_venue.html', 
       {'Venue':venue, 
       'form':form } 
    )

#search for venues
def search_venues(request):
    if request.method=="POST":
        searched = request.POST['searched']
        venues  = Venue.objects.filter(name__contains=searched)

        return render(request, 'events/search_venues.html', {
            'searched':searched,
            'venues':venues
    })
    else:
        return render(request, 'events/search_venues.html', {
    })
#show venue details
def show_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    return render(request, 'events/show_venue.html', 
       {'Venue':venue} 
    )

#list all venues
def list_venues(request):
    venue_list= Venue.objects.all().order_by('name')
    return render(request, 'events/venues.html',
        {'venue_list':venue_list})

# Create your views here.
def form(request):
    submitted = False
    if request.method =="POST":
        form = VenueForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('form?submitted = True')
    else:
        form = VenueForm
        if 'submitted' in request.GET:
            submitted = True
            return render(request, 'events/form.html', {'form':form, 'submitted':submitted})

    form = VenueForm
    return render(request, 'events/form.html', {
        'form':form
    }
    )

#home page
def home(request, year=datetime.now().year, month=datetime.now().strftime("%B")):
    name = "jon"
    month = month.capitalize()
    #covert month from name to number
    month_number = list(calendar.month_name).index(month)
    month_number - int(month_number)
    # creat calender

    cal = HTMLCalendar().formatmonth(
        year,
        month_number,
    )

    #get current year
    now = datetime.now()
    current_year = now.year

    # get current time
    time = now.strftime('%I:%M:%p')
    return render(request, 'events/home.html', {
        "name": name,
        "year": year,
        "month":month,
        "month_number":month_number,
        "cal":cal,
        "current_year":current_year,
        "time":time
    })


def all_events(request):
    event_list = Event.objects.all().order_by('name')
    return render(request, 'events/event_list.html',{
        'event_list':event_list,
    })



