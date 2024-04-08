# 📪 FAQ

## Q: Why we need ModelGo licenses?

ModelGo licenses offer flexible options to fulfill your specific licensing needs about using and distributing your deep learning models while protecting your Intellectual Property (IP). Traditional open-source software (OSS) licenses lack clear definitions regarding machine learning concepts, such as Models, Output, and Derivatives created through knowledge transfer. This lack of compatibility can result in certain ML activities (e.g., Distillation, Mix-of-Expert) being beyond the control of the model owner and potentially compromising their IP rights.

Many developers on [HuggingFace](https://huggingface.co/models?license=license:cc-by-nc-nd-4.0\&sort=likes) have chosen to use Creative Commons Licenses (CCs) to restrict commercial use of their models. However, CCs are primarily designed for artifacts such as articles, music, and pictures, making them incompatible when applied to ML models. Therefore, there is a need for a new specific licensing method for models.

Recently, Responsible AI Licenses (RAILs) have been widely advocated to address the need for governing AI technologies, aiming to restrict unlawful and unethical uses of models. We acknowledge the emerging need for such governance (which is why we offer the RAI option in ModelGo licenses), but we also recognize the demand for stricter restrictions, such as prohibiting commercial use, sharing of derivatives, and mandatory open-sourcing to protect the profits of model developers. This is why we propose ModelGo and offer more licensing options to fill this gap.

## Q: What is the difference between ModelGo and OpenRAILs?

From the compositional perspective, OpenRAILs(-M) is built upon Apache-2.0 with additional terms tailored for ML fields. Their main alterations include adding a Use Restrictions attachment and use-based behaviour restriction terms in the license text.  To offer more comprehensive licensing control, ModelGo is not solely based on Apache-2.0 but also draws inspiration or terms from GPL-3.0, CCs, AFL-3.0, Llama2 Community License, SEER License Agreement, and, of course, OpenRAILs.

From a goals perspective, OpenRAILs(-M) advocate for protecting models from unlawful and unethical use. Recently, they provide a [license generator](https://www.licenses.ai/rail-license-generator) to generate a list of domain-specific Use Restrictions. The goals of ModelGo are somewhat different; we aim to provide a CCs-like framework for controlling the use and distribution of published models. For example, developers can freely choose the most permissive licenses like MG0 and MG-BY to waive most restrictions on their models, or they can choose the NC option (which is revocable) to prevent undesired commercialization of their models and generated content. The OS option aims to incentivize sharing and contributions.

Roughly speaking, MG-BY-RAI can be seen as similar to OpenRAILs. But we just leave the RAI as a choice to the model publishers. Additionally, to further deter misuse of models, the patent use rights granted by MG-BY-RAI are revocable, distinguishing it from OpenRAILs.

## Q: What is the scope of ModelGo licenses governing?

MG licenses only apply to the Model, but their terms govern the <mark style="color:purple;">use and distribution of the Model and its derivatives, as well as outputs thereof, and complementary code and scripts</mark>. We classify these objects into three categories to define the scope of terms: Licensed Materials, Derivatives, and Output, each with different restriction terms and using policies. For example, according to the terms of MG-BY-ND, sharing the verbatim copy of Licensed Materials is allowed while sharing any Derivatives and Outputs is prohibited.

MG licenses should not apply to Third-Party Materials (e.g., open-source software and free-content artifacts), system libraries, and datasets (e.g., training set, validation set, test set). This implies that choosing MG with OS does not mandate open-sourcing the data used to develop the model. Due to data privacy concerns and the likelihood that these datasets or the data samples therein already have free-content licenses (typically CCs), we consider datasets to be outside the scope of MG licenses.

<figure><img src="../.gitbook/assets/scope.jpg" alt=""><figcaption><p>MG Governing Scope</p></figcaption></figure>

## Q: May I distribute the generated content?

You can share the generated content (including the output of the Model and the output of the Derivatives of the Model) only if the <mark style="color:purple;">ND option is not being used</mark>. MG licenses will not be proliferated to the generated content and do not claim copyright over them. However, MG licenses require users to acknowledge that the output contains AI-generated content created by the users using the model. Please refer to the "<mark style="color:purple;">The Output You Generate</mark>" section for more information.

## Q: Revocable vs. Irrevocable;  Sublicensable vs. Non-sublicensable.

Grant of patent license:

<table><thead><tr><th width="331">License Name</th><th width="200">Revocable?</th><th>Sublicensable?</th></tr></thead><tbody><tr><td>AFL-3.0</td><td><mark style="color:orange;">Not Stated</mark></td><td>Yes</td></tr><tr><td>GPL-3.0</td><td><mark style="color:orange;">Not Stated</mark></td><td>Auto Licensing</td></tr><tr><td>Apache-2.0</td><td>No</td><td><mark style="color:orange;">Not Stated</mark></td></tr><tr><td>CodeML-OpenRAIL-M</td><td>No</td><td><mark style="color:orange;">Not Stated</mark></td></tr><tr><td>CreativeML-OpenRAIL-M</td><td>No</td><td><mark style="color:orange;">Not Stated</mark></td></tr><tr><td>CC-BY-4.0</td><td>N.A.</td><td>N.A.</td></tr><tr><td>Llama2 Community License</td><td><mark style="color:orange;">Not Stated</mark></td><td><mark style="color:orange;">Not Stated</mark></td></tr><tr><td>Llama License Agreement</td><td><mark style="color:orange;">Not Stated</mark></td><td><mark style="color:orange;">Not Stated</mark></td></tr><tr><td>SEER License Agreement</td><td><mark style="color:orange;">Not Stated</mark></td><td><mark style="color:orange;">Not Stated</mark></td></tr></tbody></table>

Grant of copyright license:

<table><thead><tr><th width="331">License Name</th><th width="200">Revocable?</th><th>Sublicensable?</th></tr></thead><tbody><tr><td>Apache-2.0</td><td>No</td><td>Yes</td></tr><tr><td>CodeML-OpenRAIL-M</td><td>No</td><td>Yes</td></tr><tr><td>CreativeML-OpenRAIL-M</td><td>No</td><td>Yes</td></tr><tr><td>GPL-3.0</td><td>No</td><td>Auto Licensing</td></tr><tr><td>CC-BY-4.0</td><td>No</td><td>Auto Licensing</td></tr><tr><td>Llama License Agreement</td><td>Yes</td><td>No</td></tr><tr><td>SEER License Agreement</td><td>Yes</td><td>No</td></tr><tr><td>AFL-3.0</td><td><mark style="color:orange;">Not Stated</mark></td><td>Yes</td></tr><tr><td>Llama2 Community License</td><td><mark style="color:orange;">Not Stated</mark></td><td><mark style="color:orange;">Not Stated</mark></td></tr></tbody></table>
