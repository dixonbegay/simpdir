from django.db.models import Q, query
from django.shortcuts import render
from django.views.generic import DetailView, ListView
from django_phonedir.models import Contact, Department


def home_view(request):
    departments = Department.objects.order_by("name")
    return render(request, "home.html", {"departments": departments})


class DepartmentListView(ListView):
    model = Department
    template_name = "departments_listing.html"
    context_object_name = "departments"
    ordering = "name"

    # def get_queryset(self, *args, **kwargs):
    # We prefetch 'contacts' to avoid the N+1 query problem
    # return Department.objects.prefetch_related("contacts").all()


class DepartmentDetailView(DetailView):
    model = Department
    template_name = "department_detail.html"
    slug_field = "short_name"
    slug_url_kwarg = "short_name"


class SearchResultsView(ListView):
    model = Contact
    template_name = "search_contact_results.html"
    context_object_name = "contacts"

    def get_queryset(self) -> query.QuerySet[Contact]:
        q = self.request.GET.get("q", "")
        if not q:
            return Contact.objects.none()
        return Contact.objects.filter(
            Q(last_name__icontains=q) | Q(first_name__icontains=q)
        ).order_by("last_name")
