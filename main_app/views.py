import os
import xlsxwriter
import datetime

from io import BytesIO

from django.conf import settings
from django.db.models import Q
from django.http import HttpResponse, Http404, StreamingHttpResponse

from django.views import generic
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from . import forms
from . import models


class DownloadReportView(generic.FormView):
    form_class = forms.ReportForm
    template_name = 'download_report.html'

    def form_valid(self, form):
        year = form.cleaned_data['year']
        month = form.cleaned_data['month']

        creations = query_validator(month, year)

        total_downloads = 0

        for creation in creations:
            total_downloads += creation.total_downloads

        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()

        creation_list_text = workbook.add_format({
            'font_color': 'green',
            'font_size': 15,
            'align': 'center',
            'valign': 'vcenter',
            'color': 'green',
        })

        align_left = workbook.add_format({
            'align': 'left'
        })

        bordering = workbook.add_format({
            'border': 1
        })

        title = workbook.add_format({
            'bold': 1,
            'align': 'center',
            'border': 1,
        })

        worksheet.merge_range('B7:C7', 'Бүтээлийн жагсаалт', creation_list_text)

        bold = workbook.add_format({'bold': True})

        worksheet.write('A2', 'Нийт нэмэгдсэн:', bold)
        worksheet.write('B2', creations.count(), align_left)
        worksheet.write('A3', 'Нийт татагдсан:', bold)
        worksheet.write('B3', total_downloads, align_left)

        row = 8
        col = 0
        sel = 1

        worksheet.set_column('A:A', 20)
        worksheet.set_column('B:B', 50)
        worksheet.set_column('C:C', 15)
        worksheet.set_column('D:D', 20)
        worksheet.set_column('E:E', 10)
        worksheet.set_column('F:F', 15)
        worksheet.set_column('G:G', 10)
        worksheet.set_column('H:H', 15)

        date_format = workbook.add_format({'num_format': 'yyyy-mm-d', 'border': 1, 'align': 'center'})

        worksheet.write('A8', '№', title)
        worksheet.write('B8', 'Гарчиг', title)
        worksheet.write('C8', 'Зохиолч', title)
        worksheet.write('D8', 'Бүтээлийн төрөл', title)
        worksheet.write('E8', 'Үнэ', title)
        worksheet.write('F8', 'Бичигдсэн он', title)
        worksheet.write('G8', 'Таталт', title)
        worksheet.write('H8', 'Огноо', title)

        for obj in creations:
            worksheet.write(row, col, sel, bordering)
            worksheet.write(row, col + 1, obj.title, bordering)
            worksheet.write(row, col + 2, obj.author.get_short_name(), bordering)
            worksheet.write(row, col + 3, obj.type, bordering)
            worksheet.write(row, col + 4, obj.price, bordering)
            worksheet.write(row, col + 5, obj.created_date, date_format)
            worksheet.write(row, col + 6, obj.total_downloads, bordering)
            worksheet.write(row, col + 7, obj.uploaded_date, date_format)

            row += 1
            sel += 1

        workbook.close()
        output.seek(0)

        response = StreamingHttpResponse(
            output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=tailan.xlsx'

        return response


class AuthorDetailView(generic.DetailView):
    model = models.Author

    def get(self, request, *args, **kwargs):
        resp = super().get(request, *args, **kwargs)

        author = get_object_or_404(models.Author, pk=kwargs['pk'])

        if not request.session.session_key:
            request.session.save()

        if not models.ViewHit.objects.filter(model=author,
                                             session=request.session.session_key):
            view = models.ViewHit(model=author,
                                  ip=request.META['REMOTE_ADDR'],
                                  created=datetime.datetime.now(),
                                  session=request.session.session_key)

            view.save()

        return resp

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = context['object']
        total_downloads = 0
        total_creation_views = 0

        for creation in author.creations.all():
            total_downloads += creation.total_downloads
            total_creation_views += creation.views.count()

        context['creation_downloads'] = total_downloads
        context['creation_views'] = total_creation_views

        context['views'] = models.ViewHit.objects.filter(model=author).count()

        return context


class CreationCreateView(generic.CreateView):
    form_class = forms.CreationFormView
    template_name = 'main_app/creation_form.html'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class CreationDetailView(generic.DetailView):
    model = models.Creation

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        model = get_object_or_404(models.Creation, pk=kwargs['pk'])

        if not request.session.session_key:
            request.session.save()

        if not models.CreationViewHit.objects.filter(model=model,
                                                     session=request.session.session_key):
            view = models.CreationViewHit(model=model,
                                          ip=request.META['REMOTE_ADDR'],
                                          session=request.session.session_key,
                                          created=datetime.datetime.now())
            view.save()

        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['views'] = models.CreationViewHit.objects.filter(model=context['object']).count()

        return context


class CreationListView(generic.ListView):
    model = models.Creation

    def get_queryset(self):
        lists = models.Creation.objects.all()
        query = self.request.GET.get('query')

        if query:
            lists = models.Creation.objects.filter(
                Q(title__icontains=query) |
                Q(keyword__icontains=query) |
                Q(co_authors__icontains=query)
            )

        return lists

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(**kwargs)

        data['query'] = self.request.GET.get('query')
        data['query_count'] = len(data['object_list'])

        return data


def creation_download(request, pk=id):
    creation = models.Creation.objects.get(pk=pk)

    if creation.is_paid():
        context = {
            'object': creation
        }
        return render(request, 'payment.html', context=context)
    else:
        try:
            path = creation.file.path
        except ValueError as e:
            raise Http404
        else:
            file_path = os.path.join(settings.MEDIA_ROOT, path)
            if os.path.exists(file_path):
                with open(file_path, 'rb') as fh:
                    response = HttpResponse(fh.read(), content_type='application/force-download')
                    response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)

                    creation.total_downloads += 1
                    creation.save()

                    return response
            else:
                raise Http404


def query_validator(month, year):
    whole = 'Бүгд'
    if year != whole and month != whole:
        creations = models.Creation.objects.filter(uploaded_date__year=year,
                                                   uploaded_date__month=month)
    elif year != whole and month == whole:
        creations = models.Creation.objects.filter(uploaded_date__year=year)
    elif year == whole and month != whole:
        creations = models.Creation.objects.filter(uploaded_date__month=month)
    else:
        creations = models.Creation.objects.all()
    return creations
