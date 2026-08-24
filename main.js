const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
if (!reduced && 'IntersectionObserver' in window) {
  const sections = document.querySelectorAll('.featured-project, .project-card, .case-head, .case-layout, .about > *, .contact > *');
  sections.forEach((element) => element.classList.add('reveal'));
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.08 });
  sections.forEach((element) => observer.observe(element));
}

import { createClient } from 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/+esm';
import { SUPABASE_URL, SUPABASE_PUBLISHABLE_KEY } from './supabase-config.js';
const contactForm=document.querySelector('#contact-form'),contactStatus=document.querySelector('#contact-status'),supabase=createClient(SUPABASE_URL,SUPABASE_PUBLISHABLE_KEY);
contactForm?.addEventListener('submit',async event=>{event.preventDefault();const formData=new FormData(contactForm);if(formData.get('website'))return;const button=contactForm.querySelector('button[type="submit"]');button.disabled=true;contactStatus.className='form-status';contactStatus.textContent='正在安全送出訊息…';const{error}=await supabase.from('contact_submissions').insert({name:formData.get('name')?.trim(),email:formData.get('email')?.trim(),company:formData.get('company')?.trim()||null,subject:formData.get('subject'),message:formData.get('message')?.trim()});if(error){contactStatus.classList.add('is-error');contactStatus.textContent='目前無法送出，請稍後再試。'}else{contactForm.reset();contactStatus.classList.add('is-success');contactStatus.textContent='訊息已送出，謝謝你的聯絡！'}button.disabled=false});
