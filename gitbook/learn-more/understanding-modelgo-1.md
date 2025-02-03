---
hidden: true
---

# 📖 Understanding ModelGo

## How It's Built

ModelGo licenses are not starting from scratch; they are a remix of many successful licenses, including <mark style="color:purple;">Apache-2.0, Academic Free License 3.0 (AFL-3.0), GNU General Public License 3.0 (GPL-3.0), Creative Commons Licenses (CCs) and Open Responsible AI Licenses (OpenRAILs)</mark>. In particular, we borrow the definitions of deep learning objects from OpenRAILs, License Elements concepts from CCs, Open Source concepts from GPL, and some patent, copyright, and other legal terms from AFL and Apache. The drafting process of ModelGo also references some proprietary licenses or agreements such as Llama2 Community License, SEER License Agreement, and OpenAI's Terms of Use. However, no verbatim copy of these texts appears in our ModelGo licenses.

Our way of reusing these licenses text is compliant, and to address any copyright concerns, we disclose all referenced licenses' conditions related to reusing their text:

{% tabs %}
{% tab title="Apache-2.0" %}
> You may re-use our license unchanged, and also modify it. If you modify it, you are on your own from a legal point of view, and the result is NOT the Apache License, just a new license inspired by ours. This means that the terms 'Apache License', 'Apache', and any similar references to the ASF cannot appear in your modified license, other than to state that it differs from the original. Also, you cannot use 'Apache' in the name of the modified license. Names like "Apache License with such-and-such clause", for example, are not acceptable, as they cause confusion. Creating a new license is a non-trivial task. If you do that we recommend that you get your own legal advice. [\[Source\]](https://www.apache.org/foundation/license-faq.html#mod-license)
{% endtab %}

{% tab title="AFL-3.0" %}
> You may modify the text of this License and copy, distribute or communicate your modified version (the "Modified License") and apply it to other original works of authorship subject to the following conditions: (i) You may not indicate in any way that your Modified License is the "Academic Free License" or "AFL" and you may not use those names in the name of your Modified License; (ii) You must replace the notice specified in the first paragraph above with the notice "Licensed under " or with a notice of your own that is not confusingly similar to the notice in this License; and (iii) You may not claim that your original works are open source software unless your Modified License has been approved by Open Source Initiative (OSI) and You comply with its license review and certification process. [\[Source\]](https://opensource.org/license/afl-3-0-php)
{% endtab %}

{% tab title="GPL-3.0" %}
> It is possible to make modified versions of the GPL, but it tends to have practical consequences. You can legally use the GPL terms (possibly modified) in another license provided that you call your license by another name and do not include the GPL preamble, and provided you modify the instructions-for-use at the end enough to make it clearly different in wording and not mention GNU (though the actual procedure you describe may be similar). [\[Source\]](https://www.gnu.org/licenses/gpl-faq.en.html#ModifyGPL)
{% endtab %}

{% tab title="CCs" %}
> CC does not assert copyright in the text of its licenses, so you are permitted to modify the text as long as you do not use the CC marks to describe it. However, we do not recommend this. We also advise against [modifying our licenses](https://wiki.creativecommons.org/wiki/Modifying_the_CC_licenses) through indirect means, such as in your terms of service. A modified license very likely will not be compatible with the same CC license (unmodified) applied to other material. This would prevent licensees from using, combining, or remixing content under your customized license with other content under the same or compatible CC licenses. [\[Source\]](https://creativecommons.org/faq/#can-i-change-the-license-terms-or-conditions)
{% endtab %}

{% tab title="OpenRAILs" %}
> The BigCode OpenRAIL-M (i.e. the document itself) is licensed under a CC-BY-4.0. You can use it for your models or modify it for your own needs. [\[Source\]](https://www.bigcode-project.org/docs/pages/bigcode-openrail/#can-i-use-the-license-agreement-for-my-own-models)
{% endtab %}
{% endtabs %}

It's worth mentioning that during the drafting of ModelGo, we discovered that text reuse is common in open software licenses, and it can be difficult to identify <mark style="color:purple;">implicit copying</mark> to text from licenses that forbid reuse. Therefore, there may still be an unknown risk of copyright infringement in ModelGo licenses. Please inform us if you identify these risks or any other similar risks.

## Structure

ModelGo licenses consist of eight sections and one or two attachments. Section 2, "License Rights and Redistribution," is the <mark style="color:purple;">primary provision</mark> that grants patent and copyright licenses and states the restrictions of use and distribution. Two subsections are specific to particular licensing options: "No Derivatives" for "ND" and "Responsible Use of AI" for RAI.

ModelGo licenses include a Disclaimer of Warranty and Limitation of Liability (Section3, 4), and disclaiming any warranty of Third-Party Materials (Section 6). Additionally, our licenses include terms, as  stated in Section 7, that allow you to modify the license text, provided you furnish a readable notice describing your modifications to this license.&#x20;

The attachment, which is separate from the Terms and Conditions of the license, consists of a [Model Sheet](../get-started/how-to-choose.md#with-the-help-of-modelsheet) or, in addition, a list of Use Restrictions. Your custom restriction terms can be added to the Use Restrictions list, but changes made to the Model Sheet will not affect the license content.

<figure><img src="../.gitbook/assets/structure.jpg" alt=""><figcaption><p>Structure of MG Licenses</p></figcaption></figure>

## Timeline



<table><thead><tr><th width="135">Time</th><th>Event</th></tr></thead><tbody><tr><td>2024-11-26</td><td>Version 2.0 (a complete redraft) is now ready for release !!</td></tr><tr><td>2024-7-9</td><td>We are seeking advice from law firms.</td></tr><tr><td>2024-4-14</td><td>We are seeking legal collaboration to improve ModelGo Licenses.</td></tr><tr><td>2024-3-25</td><td>ModelGo Licenses website is online !!</td></tr><tr><td>2024-3-12</td><td><mark style="color:purple;"><strong>Moming</strong></mark> completed the 1.0 version of ModelGo licenses.</td></tr><tr><td>2024-1-23</td><td>ModelGo was accepted by ACM TheWebConf24 for an <a href="https://dl.acm.org/doi/abs/10.1145/3589334.3645520"><mark style="color:purple;"><strong>oral</strong></mark></a> presentation !</td></tr><tr><td>2023-11-13</td><td><a href="https://scholar.google.com/citations?user=vEWocfwAAAAJ"><mark style="color:purple;"><strong>Moming</strong></mark></a> and <a href="https://scholar.google.com/citations?user=RogYLKYAAAAJ"><mark style="color:purple;"><strong>Bingsheng</strong></mark></a> came up with the idea of creating a new model license for public use.</td></tr><tr><td>2023-10-5</td><td>Moming, Qinbin and Bingsheng submitted the paper 'ModelGo: A Practical Tool for Machine Learning License Analysis' to ACM <a href="https://www2024.thewebconf.org">TheWebConf24</a>.</td></tr></tbody></table>

