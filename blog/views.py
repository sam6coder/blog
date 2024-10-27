from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import date
from .models import Post
from django.views.generic import ListView,DetailView
from .forms import CommentForm
from django.views import View
# Create your views here.


# all_posts=[
#     {
#     "slug":"trip-to-the-mountains",
#     "image":"manali.jpeg",
#     "author":"Sanskriti",
#     "date":date(2024,8,31),
#     "title":"Trip To Mountains",
#     "excerpt":"A trip to Solang Valley  is a journey through the picturesque landscapes of the Himalayas,breathtaking beauty, snow-capped peaks, and a plethora of adventure activities .",
#     "content":"""A trip to Solang Valley  is a journey through the picturesque landscapes of the Himalayas,breathtaking beauty, snow-capped peaks, and a plethora of adventure activities 
#     .As we drove from Manali, the road wound through dense forests, alongside the gurgling Beas River, and past quaint mountain villages. The crisp mountain air and the sight of snow-capped 
#     peaks in the distance heightened my anticipation.  """
# },
#         {
#     "slug":"trip-to-the-rishikesh",
#     "image":"rishi.jpeg",
#     "author":"Sanskriti",
#     "date":date(2024,8,31),
#     "title":"Trip To Holy Place",
#     "excerpt":"My trip to Rishikesh was an experience that left an indelible mark on my soul, offering a perfect escape from the hustle and bustle of daily life.",
#     "content":"""The journey to Rishikesh began with a scenic drive through winding roads flanked by lush greenery. As we approached the town, the landscape gradually
#     transformed into a more rugged terrain, with the majestic Himalayas looming in the distance. The sight of the Ganges flowing gently alongside the road was a soothing 
#     prelude to the spiritual and adventurous experiences that awaited us."""
# },
#             {
#     "slug":"trip-to-the-meghalaya",
#     "image":"meghalaya.jpeg",
#     "author":"Sanskriti",
#     "date":date(2024,8,31),
#     "title":"Trip To North East",
#     "excerpt":"My trip to Meghalaya was an unforgettable experience, filled with the beauty of lush green hills, cascading waterfalls, and the warmth of the local people. ",
#     "content":"""Meghalaya, often referred to as the "Abode of Clouds," is a state in northeastern India known for its breathtaking landscapes, rich culture, and unique natural 
#     wonders. It was a journey that connected me with nature in its purest form and offered a glimpse into a way of life that is both simple and deeply rooted in tradition. 
#     The trip began in Shillong, the capital of Meghalaya, often called the "Scotland of the East" due to its rolling hills and pleasant climate. Shillong welcomed us with its 
#     mist-covered hills, pine trees, and colonial-era architecture. The city's vibrant markets, such as Police Bazaar, offered a taste of the local culture, with handicrafts, 
#     traditional clothing, and local delicacies like momos and jadoh (a rice and meat dish) on display."""
# },
#                 {
#     "slug":"trip-to-the-mathura",
#     "image":"mathura.jpeg",
#     "author":"Sanskriti",
#     "date":date(2024,8,31),
#     "title":"Trip To Krishna JanmBhumi",
#     "excerpt":"My trip to the Mathura Ganga Ghat was a journey into the heart of devotion and tranquility, where the sacred river Ganges meets the rich history and mythology of the region.",
#     "content":"""As we arrived in Mathura, the city's vibrant energy was palpable. The streets were bustling with pilgrims, tourists, and locals, all moving towards various temples and ghats
#     . The drive through the city was a mix of modernity and tradition, with old temples standing alongside newer structures. The closer we got to the Ganga Ghat, the more the atmosphere shifted 
#     towards one of reverence and spirituality. """
# },
#                 {
#     "slug":"trip-to-the-kerala",
#     "image":"kerala.jpeg",
#     "author":"Sanskriti",
#     "date":date(2024,8,31),
#     "title":"Trip To God's own Country",
#     "excerpt":"My trip to Kerala was an experience that combined natural beauty, cultural richness, and a sense of tranquility that is hard to find elsewhere. From the misty hills of Munnar to the peaceful backwaters of Alleppey, every moment in Kerala was a celebration of nature and tradition.",
#     "content":"""The journey began in Munnar, a hill station known for its sprawling tea plantations, rolling hills, and cool climate. As we drove up the winding roads, the sight of emerald-green tea gardens stretching as far as the eye could see was mesmerizing. Munnar offered us a perfect escape
#     from the heat, with its mist-covered mountains and refreshing breeze. We visited a tea museum, where we learned about the history of tea cultivation in the region and enjoyed freshly brewed tea, rich in flavor and aroma.

#  """
# },
#                 {
#     "slug":"trip-to-the-jaipur",
#     "image":"jaipur.jpeg",
#     "author":"Sanskriti",
#     "date":date(2024,8,31),
#     "title":"Trip To Pink City",
#     "excerpt":"My trip to Jaipur was a fascinating journey through time, where I explored majestic forts, grand palaces, and bustling markets that brought the rich heritage of Rajasthan to life.",
#     "content":"""As we arrived in Jaipur, the first thing that struck me was the city's unique architecture, dominated by pink-hued buildings and walls. This color scheme, originally intended to
#     welcome the Prince of Wales in 1876, has become the city's signature. The roads were wide, the traffic lively, and the atmosphere bustling with energy. Our journey began with a visit to the
#     iconic Hawa Mahal, or "Palace of Winds," an architectural marvel with its intricate latticework and numerous small windows designed to allow royal women to observe street festivities without being seen.
#  """
# },
                
#        ]

all_posts=[
    
]
# def get_date(post):
#     return post['date']
# ''


class StartingPageView(ListView):
    template_name="blog/index.html"
    model=Post
    ordering=[
    "-date"
    ]
    context_object_name="posts"
    
    def get_queryset(self) -> QuerySet[Any]:
        QuerySet= super().get_queryset()
        data=QuerySet[:3]
        return data
    
class AllPostsView(ListView):
    template_name="blog/all-posts.html"
    model=Post
    ordering=["-date"]
    context_object_name="all_posts"
        
class PostDetail(View):
    
    def get(self,request,slug):
        post=Post.objects.get(slug=slug)
        stored_posts=request.session.get("stored_posts")
        if stored_posts is not None:
            is_saved_for_later=post.id in stored_posts
        else:
            is_saved_for_later=False       
        context={"post":post,
                 "post_tags":post.tags.all(),
                 "comment_form":CommentForm(),
                 "comments":post.comments.all().order_by("-id"),
                 "saved_for_later":is_saved_for_later}
        
        return render(request,"blog/post-detail.html",context)
    
    def post(self,request,slug):     #validate the submitted form
        post=Post.objects.get(slug=slug)
        is_saved_for_later=post.id
        comment_form=CommentForm(request.POST)  # contains the submitted data
        if comment_form.is_valid():
            comment=comment_form.save(commit=False)
            comment.post= post
            comment.save()
            return HttpResponseRedirect(reverse("post-detail-page",args=[
                slug 
            ]))

        context={"post":post,
                 "post_tags":post.tags.all(),
                 "comment_form":comment_form,
                 "comments":post.comments.all().order_by("-date"),
                 "saved_for_later":is_saved_for_later
                 }
            
        return render(request,"blog/post-detail.html",context)
    
class ReadLaterView(View):
    
    def get(self,request):
        stored_posts=request.session.get("stored_posts")
        context={}
        if stored_posts is None or len(stored_posts)==0:
            context["posts"]=[]
            context["has_posts"]=False
        else:
           posts=Post.objects.filter(id__in=stored_posts) 
           context["posts"]=posts
           context["has_posts"]=True
           
        return render(request,"blog/stored-posts.html",context)
           
    def post(self,request):
        stored_posts=request.session.get("stored_posts")  #return none if there are no stored posts
        
        if stored_posts is None:
            stored_posts=[]
            
        post_id=int(request.POST["post_id"])
            
        if post_id not in stored_posts:
            stored_posts.append(post_id)
        else:
            stored_posts.remove(post_id)
        request.session["stored_posts"]=stored_posts

            
        return HttpResponseRedirect("/") 
        

            
        
    
    
        
    
    # def get_context_data(self, **kwargs) -> dict[str, Any]:
    #     context = super().get_context_data(**kwargs)
    #     context["post_tags"] = self.object.tags.all()
    #     context["comment_form"]=CommentForm()
    #     return context
    
    

    
# def posts(request):
#     all_post=Post.objects.all().order_by("-date")
#     return render(request,"blog/all-posts.html",{
#         "all_posts":all_post
#     })

# def starting_page(request):
#     latest_posts=Post.objects.all().order_by("-date")[:3]
#     # sorted_posts=sorted(all_posts,key=get_date)
#     # latest_posts=sorted_posts[-3:]
#     return render(request, "blog/index.html",{"posts":latest_posts})


# def post_detail(request,slug):
#     identify_post=get_object_or_404(Post,slug=slug)
#     return render(request,"blog/post-detail.html",{
#         "post":identify_post,
#         "post_tags":identify_post.tags.all()
#     })
