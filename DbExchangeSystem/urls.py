"""DbExchangeSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from account.views import submitRequestPage, loginPage, registerPage, logoutUser, itemRequestSearch, itemRequestViewPage, deleteItem, load_subcategories, organizationPage, itemRequestPage, discoverPage, profilePage, homePage, sendEmail, organizationSearch, submitItemPage, itemPage, itemViewPage, deleteItem2, sendEmail2, itemSearch, discoverPage2

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', loginPage, name="login"),
    path('register/', registerPage, name="register"),
    path('search_item_requests/', itemRequestSearch, name="display"),
    path('logout/', logoutUser, name="logout"),
    path('submitItemRequest/', submitRequestPage, name="submit"),
    path('view_items_requests/', itemRequestViewPage, name="viewitemrequests"),
    path('delete_item/<str:pk>/', deleteItem, name="deleteitem"),
    path('ajax/load-subcategories/', load_subcategories, name="ajax_load_subcategories"),
    path('organization_details/<str:pk>', organizationPage, name="organizationPage"),
    path('item_request_details/<str:pk>', itemRequestPage, name="itemRequestPage"),
    path('discoverItemRequests/', discoverPage, name="discoverPage"),
    path('discoverItemsAvailable/', discoverPage2, name="discoverPage2"),
    path('profile/', profilePage, name="profilePage"),
    path('home/', homePage, name="homePage"),
    path('email/<str:pk>/<str:pk2>', sendEmail, name="sendEmail"),
    path('search_organizations', organizationSearch, name="organizationSearch"),
    path('submitItem/', submitItemPage, name="submitItemPage"),
    path('item_details/<str:pk>', itemPage, name="itemPage"),
    path('view_items/', itemViewPage, name="itemViewPage"),
    path('delete2/<str:pk>', deleteItem2, name="deleteItem2"),
    path('email2/<str:pk>/<str:pk2>', sendEmail2, name="sendEmail2"),
    path('search_items/', itemSearch, name="itemSearch")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
