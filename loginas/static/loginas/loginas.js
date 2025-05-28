'use strict';

django.jQuery(document).ready(function()
{
   django.jQuery('#loginas-link').click(function()
   {
       django.jQuery('#loginas-form').submit();
       return false;
   });
});
