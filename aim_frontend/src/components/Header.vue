<template>
    <header class="mt-3">
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
                                <b-col class="col-xs-12">
                                    <div class="float-left">
                                        <a href="/static/publications/oulasvirta_et_al_2018.pdf" target="_blank">
                                            <img class="paper-thumbnail mr-5 mb-4" src="../assets/oulasvirta_et_al_2018_thumbnail.png" alt="Paper">
                                        </a>
                                    </div>
                                    <a href="/static/publications/oulasvirta_et_al_2018.pdf" target="_blank">
                                        <icon class="icon-pdf" name="file-pdf-o"></icon> PDF (1 MB)
                                    </a>
                                    <br>
                                    <span class="authors-citation">Antti Oulasvirta, Samuli De Pascale, Janin Koch, Thomas Langerak, Jussi Jokinen, Kashyap Todi, Markku Laine, Manoj Kristhombuge, Yuxi Zhu, Aliaksei Miniukovich, Gregorio Palmas, and Tino Weinkauf. 2018.</span>
                                    <span class="title-citation">Aalto Interface Metrics (AIM): A Service and Codebase for Computational GUI Evaluation.</span>
                                    <span class="release-citation">In <em>Proceedings of the 31st Annual ACM Symposium on User Interface Software and Technology Adjunct Proceedings (UIST '18 Adjunct)</em>. ACM, New York, NY, USA, 16-19. DOI: <a href="https://doi.org/10.1145/3266037.3266087" target="_blank">10.1145/3266037.3266087</a></span>
                                </b-col>
                                <b-col class="col-xs-12">
                                    <pre>
                                        <code>
@inproceedings{Oulasvirta:2018:AIM:3266037.3266087,
  author = {Oulasvirta, Antti and De Pascale, Samuli and Koch, Janin and Langerak, Thomas and Jokinen, Jussi and Todi, Kashyap and Laine, Markku and Kristhombuge, Manoj and Zhu, Yuxi and Miniukovich, Aliaksei and Palmas, Gregorio and Weinkauf, Tino},
  title = {Aalto Interface Metrics (AIM): A Service and Codebase for Computational GUI Evaluation},
  booktitle = {The 31st Annual ACM Symposium on User Interface Software and Technology Adjunct Proceedings},
  series = {UIST '18 Adjunct},
  year = {2018},
  isbn = {978-1-4503-5949-8},
  location = {Berlin, Germany},
  pages = {16--19},
  numpages = {4},
  url = {http://doi.acm.org/10.1145/3266037.3266087},
  doi = {10.1145/3266037.3266087},
  acmid = {3266087},
  publisher = {ACM},
  address = {New York, NY, USA},
  keywords = {computational evaluation, metrics, ui layouts, user interfaces},
}
                                        </code>
                                    </pre>
                                </b-col>
                            </b-row>
                        </b-modal> 
                    </b-col>
                    <b-col cols="12" class="col-lg-auto text-right">
                        <b-btn class="btn-nav btn-lg" v-b-modal.modal-project variant="link font-weight-bold">Project</b-btn>
                        <b-modal class="text-left" id="modal-project" size="lg" title="Project" ok-only ok-title="Close">
                            <b-row>
                                <b-col class="col-xs-12">
                                    <h6>Funding</h6>
                                    <p>
                                        This research has been funded by the Technology Industries of Finland Future Makers project SOWP (2017-2019) and the European Research Council starting grant (COMPUTED 2015-2020).
                                    </p>
                                    <h6>Contributors</h6>
                                    <p>
                                        Antti Oulasvirta, Samuli De Pascale, Janin Koch, Thomas Langerak, Jussi Jokinen, Kashyap Todi, Markku Laine, Manoj Kristhombuge, Yuxi Zhu, Aliaksei Miniukovich, Gregorio Palmas, and Tino Weinkauf.
                                    </p>
                                </b-col>
                            </b-row>
                        </b-modal> 
                    </b-col>
                    <b-col cols="12" class="col-lg-auto text-right last">
                        <b-btn class="btn-nav btn-lg" href="https://github.com/aalto-ui/aim" target="_blank" variant="link font-weight-bold">GitHub</b-btn>
                    </b-col>
                </b-row>
            </b-col>
        </b-row>
        <a class="link_to_top" href="#top">
            <font-awesome-icon :icon="['fas','chevron-up']" />
        </a>
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
    }
    header .title-citation {
        font-weight: 700;
    }
    header .release-citation {
    }
    header code {
        font-size: 1rem;
        font-family: monospace;
    }
    header .icon-pdf {
        margin-right: 5px;
    }
    header .btn-nav {
        padding: 0;
    }

    .link_to_top {
        position: fixed;
        bottom: 40px;
        right: 0px;
        width: 40px;
        height: 40px;
        background-color: #7553a0;
        color: #fff;
        border-radius: 3px;
        border-top-right-radius: 0;
        border-bottom-right-radius: 0;
        display: table-cell;
        text-align: center;
        padding-top: 5px;
        z-index: 1000;
    }

    .link_to_top:hover {
        background-color: #634687;
        color: #fff;
    }

    .link_to_top svg {
        vertical-align: middle;
    }

</style>