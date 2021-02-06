from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.db.models import Sum, Count
from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import get_user_model, logout, authenticate, login, update_session_auth_hash
from django.utils import timezone
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.core.paginator import Paginator
from accounts.filter import SearhPatner
from accounts.models import Profile, FriendList, ContractUs, Messeges, SuccessStory, Comment
from  accounts.forms import CommentForm,SuccessForm,PatnerSearchForm,ProfileUpdated
from accounts.tokens import account_activation_token
from accounts.forms import CompleteProfile
from django.template.loader import render_to_string
from django.http import JsonResponse
from .import filter
User=get_user_model()
# Create your views here.
def Main(request):
    import operator
    profile=Profile.objects.all().order_by("-following")
    r={}
    for p in profile:
        r[p.id]=p.following.count()
    sorted_d = dict(sorted(r.items(), key=operator.itemgetter(1), reverse=True))
    res=[]
    for i in sorted_d.keys():
        res.append(i)
    res=res[:3]
    pro =Profile.objects.filter(id__in=res).order_by('-id')
    return render(request, 'index.html',{"pro":pro})

def Signup(request):
    if request.method=="POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email_ = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if User.objects.filter(email=email_).exists():
            messages.error(request,"User Email have already used")
            return redirect("Home")
        elif password1!=password2:
            messages.error(request, "password not matching!")
            return redirect("Home")

        else:
            User.objects.create_user(
                email=email_,first_name=first_name,last_name=last_name,password=password1,
            ).save()
            msg="Registration is beign processed .Wait for Admin approval"
            messages.success(request, msg)
            return redirect("Home")
def Logout(request):
    logout(request)
    return redirect('Home')

def Login(request):
    if request.user.is_authenticated:
        return redirect('Home')
    else:
        if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['pass']
            if User.objects.filter(email=email).exists():
                if get_object_or_404(User,email=email).is_active==False:
                   messages.error(request,"Account is not active")
                   return redirect('login')
                else:
                    user = authenticate(request, email=email, password=password)
                    if user is not None:
                        login(request, user)
                        return redirect('Home')
                    else:
                        messages.error(request, "Enter correct email & password")
                        return redirect('login')
            else:
                messages.error(request, "Email is not register yet")
                return redirect('login')


        else:
            return render(request, 'login.html')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return redirect('update_profile')
    else:
        return HttpResponse('Activation link is invalid!')
def Complete_Profile(request):
    u=request.user
    if request.method=="POST":
        age = request.POST.get("age")
        height = request.POST.get("height")
        weight = request.POST.get("weight")
        mother_tongue = request.POST.get("mother_tongue")
        image = request.FILES.get("image")
        gender = request.POST.get("gender")
        marital_status = request.POST.get("marital_status")
        body_type = request.POST.get("body_type")
        complexion = request.POST.get("complexion")
        religion = request.POST.get("religion")
        physical = request.POST.get("physical")
        about = request.POST.get("about")
        drinking = request.POST.get("drinking")
        smoking = request.POST.get("smoking")
        eating = request.POST.get("eating")
        phone = request.POST.get("phone")
        whatsapp = request.POST.get("whatsapp")
        parents = request.POST.get("parents")
        country = request.POST.get("country")
        citizen = request.POST.get("citizen")
        state = request.POST.get("state")
        city = request.POST.get("city")

        education = request.POST.get("education")
        edetails  = request.POST.get("edetails")
        employee  = request.POST.get("employee")
        occupation = request.POST.get("occupation")
        aincome = request.POST.get("aincome")
        family_Value = request.POST.get("family_Value")
        family_type = request.POST.get("family_type")
        family_status = request.POST.get("family_status")
        father_status = request.POST.get("father_status")
        family_location = request.POST.get("family_location")
        about_family = request.POST.get("about_family")

        p_age = request.POST.get("p_age")
        p_height = request.POST.get("p_height")
        p_weight = request.POST.get("p_weight")
        p_mother_tongue = request.POST.get("p_mother_tongue")
        p_income = request.POST.get("p_income")
        p_occupation = request.POST.get("p_occupation")
        p_country = request.POST.get("p_country")
        p_citizenship = request.POST.get("p_citizenship")
        p_religion = request.POST.get("p_religion")
        p_physical = request.POST.get("p_physical")
        p_drinking = request.POST.get("p_drinking")
        p_smoking = request.POST.get("p_smoking")
        p_eating = request.POST.get("p_eating")
        p_education = request.POST.get("p_education")
        p_state = request.POST.get("p_state")
        p_city = request.POST.get("p_city")
        p_complexion=request.POST.get("p_complexion")
        p_body_type=request.POST.get("p_body_type")
        us =get_object_or_404(Profile,email=u)
        us.age=age
        us.height=height
        us.weight=weight
        us.mother_tongue=mother_tongue
        us.photo=image
        us.gender=gender
        us.marital_status=marital_status
        us.body_type=body_type
        us.complexion=complexion
        us.religion=religion
        us.physical_status=physical
        us.eating_habit=eating
        us.drinking_habit=drinking
        us.smoking_habit=smoking
        us.about=about
        us.phone=phone
        us.whatsapp=whatsapp
        us.parents_phone=parents
        us.country=country
        us.citizenship=citizen
        us.state=state
        us.city=city
        us.education=education
        us.education_details=edetails
        us.employed=employee
        us.occupation=occupation
        us.annual_income=aincome
        us.family_Value=family_Value
        us.family_type=family_type
        us.family_status=family_status
        us.father_status=father_status
        us.family_location=family_location
        us.about_family=about_family
        us.p_age=p_age
        us.p_height=p_height
        us.p_weight=p_weight
        us.p_city=p_city
        us.p_mother_tongue=p_mother_tongue
        us.p_education=p_education
        us.p_occupation=p_occupation
        us.p_citizenship=p_citizenship
        us.p_annual_income=p_income
        us.p_country=p_country
        us.p_religion=p_religion
        us.p_physical_status=p_physical
        us.p_eating_habit=p_eating
        us.p_drinking_habit=p_drinking
        us.p_smoking_habit=p_smoking
        us.p_state=p_state
        us.p_complexion=p_complexion
        us.p_body_type=p_body_type
        us.save()
        return redirect("dashboard")
    else:
        return render(request,'user/completd_registration.html',{"prof":u})
def ViewPage(request):
    all_post = Profile.objects.all().order_by('-id')
    myfilter =SearhPatner(request.GET,queryset=all_post)
    all_post =myfilter.qs
    all_post = Paginator(all_post, 6)
    page = request.GET.get('page')
    try:
        posts = all_post.page(page)
    except PageNotAnInteger:
        posts = all_post.page(1)
    except EmptyPage:
        posts = all_post.page(all_post.num_pages)
    context ={
        'prof':posts,
        'myfilter':myfilter,
    }
    return render(request,'Listing.html',context)
@login_required(login_url='login')
def Dashboard(request):
    return render(request,"dashboard/index.html")
def PasswordChange(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'user/change_password.html', {
        'form': form
    })

@login_required(login_url='login')
def ViewProfile(request,id):
    profile = get_object_or_404(Profile,id=id)

    if profile.viewer.filter(email=request.user.id).exists():
        pass
    else:
        profile.viewer.add(request.user)
    is_follow = False
    if profile.following.filter(email=request.user).exists():
        is_follow=True
    see_contract=False
    if profile.see_contract.filter(email=request.user).exists():
        see_contract=True
    pending_now=False
    if profile.receive_request.filter(email=request.user).exists():
        pending_now=True
    is_friend_request =False
    if profile.friend_request.filter(id=request.user.id).exists():
        is_friend_request=True
    is_friend=False
    if profile.friends.filter(id=request.user.id).exists():
        is_friend=True
    more_pro = Profile.objects.all().exclude(id=id).filter(gender=profile.gender).order_by('-id')[:4]
    edu_pro = Profile.objects.all().exclude(id=id).filter(education=profile.education).order_by('-id')[:4]

    context ={
        'is_follow':is_follow,
        'profile':profile,
        'more_pro':more_pro,
        'more_edu':edu_pro,
        'see_contract':see_contract,
        'pending':pending_now,
        'is_friend':is_friend,
        'is_friend_request':is_friend_request,
    }
    return render(request,'details.html',context)
@login_required(login_url='login')
def Follow(request):
    profile = get_object_or_404(Profile, id=request.POST.get('profile_id'))
    is_follow=False
    if profile.following.filter(email=request.user).exists():
        profile.following.remove(request.user)
        is_follow=False
    else:
        profile.following.add(request.user)
        is_follow=True
    context ={
        'is_follow': is_follow,
        'profile': profile,
    }
    if request.is_ajax():
        html = render_to_string('follow.html', context, request=request)
        return JsonResponse({'form': html})


@login_required(login_url='login')
def RequestZone(request):
    friends = FriendList.objects.filter(owner=request.user)
    add_=[]
    p=Profile.objects.filter(email=request.user)
    for s in p:
        t=s.receive_request.all()

    return render(request,'dashboard/requestzone.html',{'friends':friends,'a':t})
@login_required(login_url='login')
def ApprovedRequest(request,id):
   request_user = get_object_or_404(User,id=id)
   profile =Profile.objects.get(email=request.user)

   profile.see_contract.add(request_user)
   profile.receive_request.remove(request_user)
   profile.save()
   return redirect("requestzone")
@login_required(login_url='login')
def PendingRequest(request,id):
    request_user = get_object_or_404(User, id=id)
    owner_id = FriendList.objects.get(request_Sent=request_user)
    owner_id.contract = "Pending"
    owner_id.save()
    dat = get_object_or_404(Profile, email=request.user)
    dat.see_contract.remove(request_user)
    dat.save()
    return redirect("requestzone")
@login_required(login_url='login')
def DeleteRequest(request,id):
    request_user = get_object_or_404(User, id=id)
    profile =Profile.objects.get(email=request.user)
    profile.receive_request.remove(request_user)
    profile.save()
    return redirect("requestzone")
@login_required(login_url='login')
def SendRequest(request,id):
    profile=get_object_or_404(Profile,id=id)
    profile.receive_request.add(request.user)
    profile.save()
    return redirect(profile.get_absolute_url())

def Contract(request):
    if request.method=="POST":
        name=request.POST.get("name")
        email=request.POST.get("email")
        about=request.POST.get("about")
        ContractUs.objects.create(
            name=name,
            email=email,
            message=about
        ).save()
        messages.success(request,"your message is accepted ,wait for reply")
        return redirect('contractuse')
    return render(request,"contact.html")
@login_required(login_url='login')
def FriendsView(request):
    friends =Profile.objects.filter(email=request.user).order_by("friend_request__receive_request__email_id")
    for s in friends:
        t=s.friends.all()
    context={
        'friends':t,
    }
    return render(request,'dashboard/friendsview.html',context)
@login_required(login_url='login')
def FriendsRequestView(request):
    friends = Profile.objects.filter(email=request.user).order_by("friend_request__receive_request__email_id")
    for s in friends:
        t = s.friend_request.all()
    context = {
        'friendsrequest': t,
    }
    return render(request,'dashboard/friendrequestview.html',context)

@login_required(login_url='login')
def UnFriend(request,id):
    owner = Profile.objects.get(email=request.user)
    ownr_user = Profile.objects.get(email_id=id)
    friend = get_object_or_404(User, id=id)
    owner.friends.remove(friend)
    owner.save()
    ownr_user.friends.remove(request.user)
    ownr_user.save()
    messages.success(request,"Successfully Unfriend")
    return redirect('friends')

@login_required(login_url='login')
def RejectFriend(request,id):
    owner = Profile.objects.get(email=request.user)
    friend = get_object_or_404(User, id=id)
    owner.friend_request.remove(friend)
    owner.save()
    messages.success(request, "Successfully Reject Friend")
    return redirect('friendsrequest')

@login_required(login_url='login')
def AcceptFriend(request,id):
    owner = Profile.objects.get(email=request.user)
    ownr_user =Profile.objects.get(email_id=id)
    friend = get_object_or_404(User, id=id)
    owner.friend_request.remove(friend)
    owner.friends.add(friend)
    owner.save()
    ownr_user.friends.add(request.user)
    ownr_user.save()

    messages.success(request, "Successfully Added Friend")
    return redirect('friendsrequest')

@login_required(login_url='login')
def Messenger(request):
    message = Messeges.objects.filter(receiver=request.user).order_by("-reply_on")
    return render(request,'dashboard/messenger.html',{'inbox':message})

@login_required(login_url='login')
def SendMessage(request):
    friends = Profile.objects.filter(email=request.user)
    for s in friends:
        t = s.friends.all()
    context ={
        "fr":t,
    }
    if request.method=="POST":
        sender =request.user
        receiver = request.POST.get("to")
        subject = request.POST.get("subject")
        msg = request.POST.get("message")
        Messeges.objects.create(
            sender=sender,receiver=get_object_or_404(User,email=receiver),subject=subject,sender_msg=msg
        ).save()
        messages.success(request,"Message sent succesfully")
        return redirect("sendmessage")
    else:
        return render(request,'dashboard/composemessage.html',context)

@login_required(login_url='login')
def ViewSendMessage(request):
    message = Messeges.objects.filter(sender=request.user).order_by("-send_on")
    context ={
        'msg':message,
    }
    return render(request,'dashboard/sentmessage.html',context)

@login_required(login_url='login')
def AddFriend(request,id):
    profile=get_object_or_404(Profile,id=id)
    profile.friend_request.add(request.user)
    profile.save()
    return redirect(profile.get_absolute_url())

@login_required(login_url='login')
def RepliedMessage(request,id):
    m=Messeges.objects.get(id=id)
    sender =m.sender
    receiver = m.receiver
    msgr=''
    msgs=''
    if receiver==request.user:
        msgs =m.sender_msg
    else:
        msgr=m.receiver_msg
    if request.method=="POST":
        reply=request.POST.get("reply")
        if msgr:
            pass
        if msgs:
            m.receiver_msg=reply
            m.save()
            return redirect("messenger")
    else:
        return render(request,'dashboard/replymessage.html',{'m':m})

@login_required(login_url='login')
def ViewSendMessageDetails(request,id):
    msg = Messeges.objects.get(id=id)
    context={
        'msg':msg,
    }
    return render(request,'dashboard/viewsendmessagedetails.html',context)



def SuccesStory(request):
    success =SuccessStory.objects.all().filter(approve=True).order_by("-id")
    paginator = Paginator(success, 4)
    page = request.GET.get('page')
    scope = paginator.get_page(page)
    context ={
        'story':scope,
    }
    return render(request,'successstory.html',context)
@login_required(login_url='login')
def viewSuccessstory(request,id):
    story = SuccessStory.objects.get(id=id)
    other = SuccessStory.objects.all().filter(approve=True).order_by("-id").exclude(id=id)[:10]
    is_liked = False
    if story.likes.filter(id=request.user.id).exists():
        is_liked =True
    comments = Comment.objects.filter(post=story, reply=None).order_by('-id')
    if request.method == "POST":
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            content = comment_form.cleaned_data.get('content')
            reply_id = request.POST.get('comment_id')
            comment_qs = None
            if reply_id:
                comment_qs = Comment.objects.get(id=reply_id)
            comment = Comment.objects.create(post=story, user=request.user, content=content, reply=comment_qs)
            comment.save()
            return redirect(story.get_absolute_url())
    else:
        comment_form = CommentForm()
    context ={
        'story':story,
        'other':other,
        'total_liked':story.likes.count(),
        'is_liked':is_liked,
        'comment_form': comment_form,
        'comments': comments,
    }
    if request.is_ajax():
        html = render_to_string('comment_section.html', context, request=request)
        return JsonResponse({'form': html})
    return render(request, 'successdetails.html', context)

def Likes(request):
    story_id=request.POST.get('likes_btn')
    story=get_object_or_404(SuccessStory,id=request.POST.get('likes_btn'))
    is_liked =False
    if story.likes.filter(id=request.user.id).exists():
        story.likes.remove(request.user)
        is_liked=False
    else:
        story.likes.add(request.user)
        is_liked=True
    context = {
        'story': story,
        'total_liked': story.likes.count(),
        'is_liked': is_liked,
    }
    print(is_liked)
    if request.is_ajax():
        html = render_to_string('partial_like.html', context, request=request)
        return JsonResponse({'form': html})
@login_required(login_url='login')
def AddSuccessStory(request):
    if request.method == "POST":
        form =SuccessForm(request.POST or None,request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.post_by=request.user
            instance.save()
            messages.success(request,"Story saved successfully .Please wait for Admin Approval.")
            return redirect('addsuccess')
    else:
        form=SuccessForm()
    context ={
        'form':form,
    }
    return render(request,'user/addsuccessstory.html',context)
@login_required(login_url='login')
def StoryList(request):
    story =SuccessStory.objects.filter(post_by=request.user)
    context ={
        'story':story,
    }
    return render(request,'user/storylist.html',context)

def DeleteStory(request,id):
    story = get_object_or_404(SuccessStory, id=id)
    story.delete()
    messages.error(request,"story deleted")
    return redirect("storylist")

def UpdateStory(request,id):
    story = get_object_or_404(SuccessStory, id=id)
    if request.method=="POST":
        form = SuccessForm(request.POST or None,request.FILES,instance=story)
        if form.is_valid():
            form.save()
            messages.success(request,"story updated.")
            return redirect("storylist")

    else:
        form=SuccessForm(instance=story)
    context = {
            'form': form,
    }
    return render(request,'user/updatestory.html',context)

import csv
import designcsv
import predictmodel
import pandas as pd
@login_required(login_url='login')
def SearchPatner(request):
    user_gender=Profile.objects.get(email=request.user)
    if user_gender.redaytogo() ==True:
        u=""
        if user_gender.gender=="Male":
            u="Female"
        else:
            u="Male"

        pro =Profile.objects.all().exclude(email=request.user).values('age','height','weight','city','education','annual_income','gender','body_type','complexion','drinking_habit','smoking_habit','religion','family_status','marital_status','physical_status','email_id').filter(gender=u)
        designcsv.Createcsv(pro)
        if request.method == "POST":
            age = request.POST['age']
            height = request.POST['height']
            weight = request.POST['weight']
            weight = request.POST['weight']
            income = request.POST['income']
            city = request.POST['city']
            religion = request.POST['religion']
            complexion = request.POST['complexion']
            education = request.POST['education']
            body_type = request.POST['body_type']
            marital_status = request.POST['marital_status']
            physical = request.POST['physical']
            drinking = request.POST['drinking']
            smoking = request.POST['smoking']
            family_type = request.POST['family_type']
            temp = {}
            temp['age'] = age
            temp['height'] = height
            temp['weight'] = weight
            temp['city'] = city
            temp['education'] = education
            temp['income'] = income
            temp['gender'] = u
            temp['body_type'] = body_type
            temp['complexin'] = complexion
            temp['drinking'] = drinking
            temp['smoking'] = smoking
            temp['religion'] = religion
            temp['family_status'] = family_type
            temp['marital_status'] = marital_status
            temp['physical_status'] = physical
            try:
                result = predictmodel.tutul(temp)
                pro = Profile.objects.filter(id__in=result).filter(gender=u)
                return render(request,'sarch form.html',{'pro':pro})
            except:
                m="No Matching Found"
                return render(request, 'sarch form.html', {'mm': m})


        else:
            temp = {}
            temp['age'] = request.user.profile.p_age
            temp['height'] = request.user.profile.p_height
            temp['weight'] = request.user.profile.p_weight
            temp['city'] = request.user.profile.p_city
            temp['education'] = request.user.profile.p_education
            temp['income'] = request.user.profile.p_annual_income
            temp['gender'] = u
            temp['body_type'] = request.user.profile.p_body_type
            temp['complexin'] = request.user.profile.p_complexion
            temp['drinking'] = request.user.profile.drinking_habit
            temp['smoking'] = request.user.profile.p_smoking_habit
            temp['religion'] = request.user.profile.p_religion
            temp['family_status'] = request.user.profile.family_status
            temp['marital_status'] = request.user.profile.marital_status
            temp['physical_status'] = request.user.profile.p_physical_status
            try:
                result=predictmodel.tutul(temp)
                print(result)
                pro = Profile.objects.filter(gender=u).filter(email__in=result)
                print(pro)
                return render(request, 'sarch form.html', {'pro': pro})
            except:
                m="Not Matchhing found with your preference"
                return render(request,'sarch form.html',{'mm':m})
    else:
        print("error")
        messa="Please Completed your Profile to enjoy this feature"
        return render(request, 'sarch form.html', {'m': messa})

import SuccessRate
def SuccessRatting(request,id):
    try:
        if Profile.objects.get(id=id).gender=="Female":
            patner=Profile.objects.get(id=id)
            myself=Profile.objects.get(email=request.user)
            res=SuccessRate.Success(myself,patner)
        else:
            patner = Profile.objects.get(id=id)
            myself = Profile.objects.get(email=request.user)
            res=SuccessRate.Success(patner,myself)
    except:
        res=0

    patner = Profile.objects.get(id=id)
    context={
        'patner':patner,
        'rate':res,
    }
    return render(request,'successratting.html',context)
@login_required(login_url='login')
def UpdateP(request):
    profile=Profile.objects.get(email=request.user)
    if request.method=="POST":
        form=ProfileUpdated(request.POST or None, request.FILES, instance=profile)
        if form.is_valid():
            obj=form.save(commit=False)
            obj.email=request.user
            obj.save()
            print("done")
            return redirect('dashboard')
    else:
        form = ProfileUpdated(instance=profile)
    return render(request,'dashboard/updateprofile.html',{'form':form})