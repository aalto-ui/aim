<template>
    <header class="mt-2">
        <b-row class="align-items-end">
            <b-col class="col-auto text-left">
                <a href="http://www.aalto.fi">
                    <img id="logo-aalto" src="../assets/Aalto_EN_21_RGB_4.png" alt="Aalto University" height="150">
                </a>
            </b-col>
            <b-col class="col-auto text-left">
                <a href="http://userinterfaces.aalto.fi">
                    <img id="logo-aaltoui" src="../assets/ui_logo.png" alt="User Interfaces Group" height="50">
                </a>
            </b-col>
            <b-col class="text-right">
                <b-row>
                    <b-col cols="12" class="col-lg-auto ml-auto text-right">
                        <b-btn class="btn-nav btn-lg" href="mailto:interfacemetrics@aalto.fi?subject=Aalto%20Interface%20Metrics%3A%20Feedback" variant="link font-weight-bold">Contact</b-btn>
                    </b-col>
                    <b-col cols="12" class="col-lg-auto text-right">
                        <b-btn class="btn-nav btn-lg" v-b-modal.modal-publication variant="link font-weight-bold">Publication</b-btn>
                        <b-modal class="text-left" id="modal-publication" size="lg" title="Publication" ok-only ok-title="Close">
                            <b-row>
                                <b-col class="col-auto">
                                    <a href="/static/publications/oulasvirta_et_al_2018.pdf" target="_blank">
                                        <img class="paper-thumbnail" src="../assets/oulasvirta_et_al_2018_thumbnail.png" alt="Paper">
                                    </a>
                                </b-col>
                                <b-col class="pl-5">
                                    <p>
                                        <a href="/static/publications/oulasvirta_et_al_2018.pdf" target="_blank">
                                            <icon class="icon-pdf" name="file-pdf-o"></icon> PDF (1 MB)
                                        </a>
                                        <br>
                                        <span class="authors-citation">Antti Oulasvirta, Samuli De Pascale, Janin Koch, Thomas Langerak, Jussi Jokinen, Kashyap Todi, Markku Laine, Manoj Kristhombuge, Yuxi Zhu, Aliaksei Miniukovich, Gregorio Palmas, Tino Weinkauf</span>
                                        <span class="title-citation">Aalto Interface Metrics (AIM): A Service and Codebase for Computational GUI Evaluation</span>
                                        <span class="release-citation">In Proceedings of the 31st Annual ACM Symposium on User Interface Software and Technology (UIST '18). ACM, New York, NY, USA, 2018. DOI: <a href="https://doi.org/10.1145/3266037.3266087" target="_blank">10.1145/3266037.3266087</a></span>
                                    </p>
                                </b-col>
        <!--                         <b-col class="mt-4 col-xs-12">
                                    <pre>
                                        <code>
@inproceedings{,
  author = {},
  title = {},
  booktitle = {},
  series = {},
  year = {},
  isbn = {},
  location = {},
  pages = {},
  numpages = {},
  url = {},
  doi = {10.1145/3266037.3266087},
  acmid = {},
  publisher = {},
  address = {},
  keywords = {},
} 
                                        </code>
                                    </pre>
                                </b-col> -->
                            </b-row>
                        </b-modal> 
                    </b-col>
                    <b-col cols="12" class="col-lg-auto text-right last">
                        <b-btn class="btn-nav btn-lg" href="https://github.com/aalto-ui/aim" target="_blank" variant="link font-weight-bold">GitHub</b-btn>
                    </b-col>
                </b-row>
            </b-col>
        </b-row>
    </header>
</template>

<style>
    #logo-aalto {
        margin-left: -40px;
        margin-right: -30px;
        margin-bottom: -28px;
    }
    #logo-aaltoui {
        margin-bottom: 23px;
    }
    header .text-right.last {
        padding-bottom: 8px;
    }
    header .paper-thumbnail {
        border: 1px solid gray;
    }
    header .authors-citation {
        padding-top: 5px;
        font-style: italic;
        float: left;
    }
    header .title-citation {
        font-weight: 700;
        float: left;
    }
    header .release-citation {
        float: left;
    }
    header code {
        font-size: 1.1rem;
        font-family: monospace;
    }
    header .icon-pdf {
        margin-right: 5px;
    }
    header .btn-nav {
        padding: 0;
    }
</style>