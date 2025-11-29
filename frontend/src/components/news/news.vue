<template>
    <div>
        <nav aria-label="breadcrumb" class="continer">
                <ol class="breadcrumb">
                    <li class="breadcrumb-item"><span class="backButton"><router-link style="text-decoration: none" :to="{name: 'Home'}">Home</router-link></span></li>  
                    <li class="breadcrumb-item active" aria-current="page">news & announcements</li>
                </ol>
        </nav>
        <div class="continer">
            <div class="row">
                <h3 class="col-6">              
                    News and announcements
                </h3>
                 <!--add button on smaller devices -->
                 <div class="col-6 btn-group d-sm-block d-md-none text-right">
                        <div style="padding: 0px 0px 25px 10px">
                                <button class="btn btn-success" data-toggle="modal" data-target="#addNewsModal">                                                            
                                        <b>+</b> add          
                                </button>
                        </div>
                </div>  
            </div>
             
            <hr>
            <div class="row">
                <!-- navigation on the left -->
                <section class="col">
                    
                </section>
                <!-- content -->
                <section class="col-lg-9">
                    <article id="news">                            
                        <div class="row">                                
                            <div class="col-lg-12 " v-if="news">                                                                        
                                <div    v-for="news in news"
                                        class="border border-light shadow p-2 mb-2 bg-white rounded">
                                    <i class="text-primary font-weight-bold">{{news.author}}</i>
                                    <p class="lead">{{news.heading}}</p>   
                                    <article :id="`article_` + news.id">                                    
                                    </article>                                                                                                         
                                    <p>
                                    <i>{{$humanizeDate(news.date)}}</i>
                                    </p>
                                </div>                                        
                            </div>
                            <div class="col text-center text-muted" v-else>
                                <h3>Oops!</h3>
                                <h3>news articles not found</h3>
                                <p>add news articles to have content here</p>
                            </div>
                            
                        </div>                            
                    </article>
                </section>
                <!-- actions -->
                <section class="col-lg-2">
                    <button data-toggle="modal" data-target="#addNewsModal"
                            class="btn btn-success">
                        + Add 
                    </button>
                </section>
            </div>                      
        </div>

        <!-- MODALS -->
        <section>
            <!-- Modal -->
            <div class="modal fade" id="addNewsModal" tabindex="-1" role="dialog" aria-labelledby="addNewsModal" aria-hidden="true">
                    <div class="modal-dialog modal-dialog-centered modal-lg" role="document">
                    <div class="modal-content">
                        <div class="modal-header">
                        <h5 class="modal-title" >Add news or announcement</h5>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                        </div>
                        <div class="modal-body">
                            <label class="font-weight-bold">heading / title</label>                            
                            <input  v-model="news_title" maxlength="100"
                                    type="text" class="mb-4 form-control" 
                                    placeholder="A catchy title for your article">
                            
                            <label class=font-weight-bold>article</label> 
                            <quill-editor class="mb-4" v-model="news_article"/>

                            <label class="font-weight-bold">author</label>                            
                            <input  v-model="news_author" maxlength="100"
                                    type="text" class="mb-4 form-control" 
                                    placeholder="eg. John Doe, Church Pastor ">
                            
                        </div>
                        <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                        <button type="button" class="btn btn-success" v-on:click="addNewsArticle()">
                            add article
                            <span v-if="adding_news_article"
                                class="spinner-border spinner-border-sm" role="status" aria-hidden="true">
                            </span>
                        </button>
                        </div>
                    </div>
                    </div>
            </div>
        </section>
    </div>
</template>

<script>
export default {
    name: 'smsAnalytics',
    data () {
        return{
           news: null,
           //adding news article
           adding_news_article: false,
           news_article:null,
           news_title:null,
           news_author:null           
        }
    },
    created () {
       this.getNews() 
    },
    methods: {
        //get news
        getNews () {  
            this.$store.dispatch('update_isLoading', true)          
            this.$http.get(this.$BASE_URL + '/api/news/recent-news/')
                .then(response => {
                    this.news =  response.data                    
                    this.$store.dispatch('update_isLoading', false)                    
                    setTimeout(()=>{ this.parseNewsArticles() },3000)
                })
                .catch((err) => {
                    this.$store.dispatch('update_isLoading', false)
                    alert("error occured while fetching data:" + err )
                })
        },
        parseNewsArticles: function(){           
            for (var i in this.news){                
                //article div                       
                var article_div = document.getElementById("article_" + this.news[i].id)                                                                
                //new elements
                var el = document.createElement('div')        
                var domString = this.news[i].article
                el.innerHTML =  domString;
                article_div.appendChild(el);                

                var images = article_div.getElementsByTagName("img")                
                for (var img in images){
                    var img_el = images[img]
                    if (img_el instanceof HTMLElement){                        
                        img_el.classList.add("image-fit");  // make image to fit box
                    }                    
                }

            }        
        },
        //adding news article
        addNewsArticle: function(){
            this.adding_news_article = true
            this.$http.post(
                this.$BASE_URL + '/api/news/add-news/',
                {
                    heading:this.news_title,
                    article:this.news_article,
                    author:this.news_author
                } 
            ).then(()=>{
                this.adding_news_article = false
                this.news_article = null
                this.news_author = null
                this.news_title = null
                this.getNews()
            }).catch((err)=>{
                this.adding_news_article = false
                this.news_article = null
                this.news_author = null
                this.news_title = null
                alert("an error occured :" + err)
            })
        }
    }
}
</script>


<style >
</style>