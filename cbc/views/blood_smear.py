from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

from cbc.models import CompleteBloodCount, BloodSmear
from range.models import ReferenceRange, IndexRange

from cbc.forms import CBCModelForm, BloodSmearFormSet


class BloodSmearCreateView(CreateView):
    model = CompleteBloodCount
    template_name = 'cbc/cbc_create.html'
    form_class = CBCModelForm

    def get_success_url(self):
        return reverse_lazy('cbc:blood-smear-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(BloodSmearCreateView, self).get_context_data(**kwargs)
        user = self.request.user
        post = self.request.POST
        if post:
            context['blood_smear'] = BloodSmearFormSet(post)
        else:
            context['blood_smear'] = BloodSmearFormSet()
        if user.is_authenticated:
            context['cbc'] = CompleteBloodCount.objects.filter(user=user)
            context['blood_diagram'] = BloodSmear.objects.filter(cbc__user=user)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        blood_smear = context['blood_smear']
        cbc = form.instance
        user = self.request.user
        if form.is_valid():
            with transaction.atomic():
                cbc.content_type = ContentType.objects.get(app_label='cbc', model='bloodsmear')
                cbc.object_id = 0
                cbc.type = 9
                if user.is_authenticated:
                    cbc.user = user
                    cbc.age = user.patient.get_age()
                    cbc.sex = user.patient.sex
                self.object = form.save()
                if blood_smear.is_valid():
                    blood_smear.instance = self.object
                    blood_smear.save()
                    fd_object = BloodSmear.objects.get(cbc_id=self.object.id)
                    cbc.object_id = fd_object.id
                self.object = form.save()
        return super(BloodSmearCreateView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class BloodSmearUpdateView(UpdateView):
    model = CompleteBloodCount
    template_name = 'cbc/cbc_update.html'
    form_class = CBCModelForm

    def get_success_url(self):
        return reverse_lazy('cbc:blood-smear-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(BloodSmearUpdateView, self).get_context_data(**kwargs)
        user = self.request.user
        post = self.request.POST
        if post:
            context['blood_smear'] = BloodSmearFormSet(post, instance=self.object)
        else:
            context['blood_smear'] = BloodSmearFormSet(instance=self.object)
        if user.is_authenticated:
            context['blood_diagram'] = BloodSmear.objects.filter(cbc__user=user)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        blood_smear = context['blood_smear']
        if form.is_valid():
            with transaction.atomic():
                self.object = form.save()
                if blood_smear.is_valid():
                    blood_smear.instance = self.object
                    blood_smear.save()
        return super(BloodSmearUpdateView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class BloodSmearDetailView(DetailView):
    model = CompleteBloodCount
    template_name = 'cbc/cbc_detail.html'

    def get_context_data(self, **kwargs):
        context = super(BloodSmearDetailView, self).get_context_data(**kwargs)
        user = self.request.user
        blood_smear = BloodSmear.objects.get(cbc_id=self.object.id)
        context['blood_smear'] = blood_smear
        context['index_range'] = IndexRange.objects.filter().last()
        context['blood_diagram'] = BloodSmear.objects.filter(cbc__user=user)
        if user.is_authenticated:
            age = user.patient.get_age()
            context['range'] = ReferenceRange.objects.get(
                cbc__sex=user.patient.sex,
                cbc__age_min__lt=age,
                cbc__age_max__gt=age,
                diff__value_type=blood_smear.value_type
            )
        else:
            context['range'] = ReferenceRange.objects.get(
                cbc__sex=blood_smear.cbc.sex,
                cbc__age_min__lt=blood_smear.cbc.age,
                cbc__age_max__gt=blood_smear.cbc.age,
                diff__value_type=blood_smear.value_type
            )
        return context
