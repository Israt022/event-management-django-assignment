from django import forms
from tasks.models import Category,Event,Participant

class StyledFormMixin:
    default_classes = 'border-2 border-gray-300 text-center w-md mt-2 p-3 rounded-lg shadow-sm focus: border-orange-500 focus:ring-orange-500 focus:ring-rose-500'
    
    def apply_styled_widgets(self):
         for field_name,field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                 field.widget.attrs.update({
                     'class' : self.default_classes,
                     'placeholder' : f'Enter {field.label.lower()}',
                 })
            elif isinstance(field.widget,forms.Textarea):
                field.widget.attrs.update({
                    'class' : f'{self.default_classes} focus: resize-none',
                    'placeholder' : f'Enter {field.label.lower()}',
                    'rows' : 5
                })
            elif isinstance(field.widget,forms.EmailInput):
                field.widget.attrs.update({
                    'class' : self.default_classes ,
                    'placeholder' : f'Enter {field.label.lower()}',

                })
            elif isinstance(field.widget,forms.SelectDateWidget):
                field.widget.attrs.update({
                    'class' : 'border-2 border-gray-300 px-2 py-2  ml-2 rounded-lg shadow-sm focus: outline-none   focus: border-orange-500 focus:ring-orange-500 px-2 mt-2'
                })
            elif isinstance(field.widget,forms.TimeInput):
                field.widget.attrs.update({
                    'class' : forms.TimeInput(format='%H:%M')
                })
            elif isinstance(field.widget,forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'class' : 'space-y-2 focus: border-orange-500 focus:ring-orange-500'
                })
            elif isinstance(field.widget,forms.Select):
                field.widget.attrs.update({
                    'class' : 'mt-2 border-2 border-gray-300 p-3 rounded-lg shadow-sm focus:outline-none focus: border-orange-500 focus:ring-orange-500'
                })

class CategoryForm(StyledFormMixin,forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name','description']
          
    
    
    
    
class EventForm(StyledFormMixin,forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name','description','date','time','location','category']
        widgets = {
            'date' : forms.SelectDateWidget,
            'time' : forms.TimeInput(),
            'category' : forms.Select,
            
        }
    
    def __init__(self, *args, **kwargs):
        category = kwargs.pop('category',[])
        super().__init__(*args,**kwargs)
        self.fields['category'].choices = [
            (cat.id , cat.name) for cat in category 
        ] 
        self.apply_styled_widgets()
        
class ParticipantForm(StyledFormMixin,forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['name','email','event']
        widgets = {
            'event' : forms.CheckboxSelectMultiple
        }
    def __init__(self, *args, **kwargs):
        events = kwargs.pop('events',[])
        super().__init__(*args,**kwargs)
        self.fields['event'].choices = [
            (event.id , event.name) for event in events 
        ] 
        self.apply_styled_widgets()

class StyledFormMixin:
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)  
        self.apply_styled_widgets()
        
    default_classes = 'mt-5 border-2 border-gray-300 w-full p-3 rounded-lg shadow-sm focus:outline-none focus:border-rose-500 focus:ring-rose-500'
    
    def apply_styled_widgets(self):
         for field_name,field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                 field.widget.attrs.update({
                     'class' : self.default_classes,
                     'placeholder' : f'Enter {field.label.lower()}'
                 })
            elif isinstance(field.widget,forms.Textarea):
                field.widget.attrs.update({
                    'class' : f'{self.default_classes} focus: resize-none',
                    'placeholder' : f'Enter {field.label.lower()}',
                    'rows' : 5
                })
            elif isinstance(field.widget,forms.EmailInput):
                field.widget.attrs.update({
                    'class' : self.default_classes,
                    'placeholder' : f'Enter {field.label.lower()}',
                })
            elif isinstance(field.widget,forms.SelectDateWidget):
                field.widget.attrs.update({
                    'class' : 'border-2 border-gray-300  p-3  rounded-lg shadow-sm focus: outline-none   focus: border-rose-500 focus:ring-rose-500'
                })
            elif isinstance(field.widget,forms.TimeInput):
                field.widget.attrs.update({
                    # 'class' : 'border-2 border-gray-300  p-3  rounded-lg shadow-sm focus: outline-none'
                    'class' : forms.TimeInput(format='%H:%M'),
                })
            elif isinstance(field.widget,forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'class' : 'space-y-2'
                })
            elif isinstance(field.widget,forms.Select):
                field.widget.attrs.update({
                    'class' : 'border-2 border-gray-300  p-3  rounded-lg shadow-sm focus: outline-none   focus: border-rose-500 focus:ring-rose-500 '
                })
            else:
                print("Inside else")
                field.widget.attrs.update({
                    'class': self.default_classes
                })