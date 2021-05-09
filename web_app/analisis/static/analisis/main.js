$(document).ready(function() {
	function renderTweet(divId, tweetOptions){
		// https://developer.twitter.com/en/docs/twitter-for-websites/javascript-api/guides/scripting-factory-functions
		twttr.widgets.createTweet(
			document.getElementById(divId).dataset.tweetId,
			document.getElementById(divId),
			tweetOptions
		)
		.then(function(el){
			if(el == undefined){
				console.info(`The tweet ${divId} is not available. Display text instead.`);
				document.getElementById(divId).textContent = document.getElementById(divId).dataset.tweetText;
			}
		})

	}

	//Render tweets
	twttr.ready(function() {
		let tweetOptions = { align: "center", width: "325", dnt: true, conversation: "none"}

		renderTweet('tweetTarget', tweetOptions);
		renderTweet('tweetResponse', tweetOptions);
	});


	var START_TIME = new Date();
	$('#mainForm').on('submit',function(){
		var checkboxes = document.querySelectorAll('input[type="checkbox"]');
		var checkedOne = Array.prototype.slice.call(checkboxes).some(x => x.checked);
		if(!checkedOne){
			alert('Debe seleccionar al menos una opcion. En preguntas de opción múltiple.')
			return false;
		}

		var time_spent = dateDiffInSecond(START_TIME, new Date());
		addFieldsToForm('time_spent',time_spent);
		$("#mainFormSubmitButton").attr('disabled', true);
		return true;

		function addFieldsToForm(name, value){
			$("<input/>")
				.attr("type", "hidden")
				.attr("name", name)
				.attr("value", value)
				.appendTo("#mainForm");
		}

		function dateDiffInSecond(startDate, endDate){
			var timeDiff = Math.abs(endDate.getTime() - startDate.getTime()); // in miliseconds
			var timeDiffInSecond = Math.ceil(timeDiff / 1000); // in second
			return timeDiffInSecond;
		}
	});

	// Component for showing previous answers on a given question.
	Vue.component('previous-answers', {			
		props : ['questionId'],		
		delimiters : ['#[[',']]'],
		data() {
			return {
				answers: []
			}			
		},		
		computed: {
			helpText: function(){	
				result = this.answers
				.map(x => {
					x.value = JSON.stringify(x.value_json)
					return x
				})
				.map(x => `<li>Annotation:${x.annotation}. Answer: ${x.value}</li>`)
				.join('')
				result = `<ul>${result}</ul>`
				return result
			} 
		},
		methods : {
			fetchAnswers(){
				const URL=`/api/answers/?question.id=${this.questionId}&tweet_relation.id=${this.$store.state.tweetRelationId}`
				fetch(URL)
					.then(stream => stream.json())
					.then((data) => this.answers = data)					
					.then(() => console.log(this.answers))
                    .catch(error => console.error(error))
			}
		},
		mounted() {
			$('[data-toggle="popover"]').popover();
			this.fetchAnswers()
		},
		template: `
		<button  v-if="this.$store.state.showPreviousAnswers==true"
			type="button" 
			class="btn btn-secondary btn-sm" 			
			data-html="true" 
			data-container="body" 
			data-toggle="popover" 
			data-placement="top" 
			:data-content="helpText" >
  			previous answers
		</button>
		`
	})
	
	// Component for the question "¿De qué país se habla en el tweet original?"
	Vue.component('question-block-target-tweet-country', {		
		props : ['question','options'],
		delimiters : ['#[[',']]'],
		methods : {
			handler: function(e){
				if (e.target.value === 'No es claro' && e.target.checked === true){
					this.$el.querySelectorAll('input:not([value="No es claro"])').forEach(function(elem){
						elem.checked=false
						elem.disabled = true
					})
				}else if (e.target.value === 'No es claro' && e.target.checked === false){
					this.$el.querySelectorAll('input:not([value="No es claro"])').forEach(function(elem){
						elem.disabled = false
					})
				}
			}
		},
		template: `
		<div>
			<h6> 
				#[[ question.value ]] 
				<previous-answers 
				:questionId="question.id"
				>
				</previous-answers> 
			</h6>
			<ul class="list-unstyled card-columns">
				<li class="form-check" v-for="option in options">
					<input 
						class="form-check-input"
						type="checkbox"
						:name="question.id"
						:value="option"
						@change="handler"
					>
					<label class="form-check-label"> #[[ option ]] </label>
				</li>
			</ul>
		</div>
		`
	})

	// Component for one-choice questions without any additional logic
	var questionBlock = Vue.component('question-block', {
		props : ['question','options','show'],
		delimiters : ['#[[',']]'],
		methods: {
			handler: function(e){}
		},
		template: `
		<div v-if="show==true || show == undefined">
			<h6> 
			#[[ question.value ]] 
			<previous-answers 
			:questionId="question.id"
			>
			</previous-answers> 
			</h6>
			<ul class="list-unstyled card-columns">
				<li class="form-check" v-for="option in options">
					<input 
						class="form-check-input"
						type="radio"
						:name="question.id"
						:value="option"
						@change="handler"
						required
					>
					<label class="form-check-label"> #[[ option ]] </label>
				</li>
			</ul>
		</div>
		`
	})

	// Component for the one-choice question "¿Cuál es la postura del tweet respuesta al contenido del tweet original?"
	Vue.component('question-block-stance-of-response-to-target-content',{
		extends: questionBlock,
		methods: {
			handler: function(e){
				this.$emit('stancechanged', e.target.value)
			}
		},
	})
	
	// Component for the one-choice question "¿La respuesta expresa que el original contiene información verdadera?"
	var questionBlockTrueNews = Vue.component('question-block-true-news',{
		extends: questionBlock,
		methods: {
			handler: function(e){
				this.$emit('evidencechanged', e.target.value)
			}
		},
	})

	// Component for the one-choice question "¿La respuesta expresa que el original contiene información falsa?"
	Vue.component('question-block-fake-news',{ extends: questionBlockTrueNews })


	Vue.component('section-collapsible', {
		props : ['section'],
		delimiters : ['#[[',']]'],
		data() {
			return {
				stance: '', //model for the last section of questions
				evidence: '', 
			}			
		},
		computed: {
			showTrueNewsQuestion: function(){
				return this.stance==='Soporte Explícito' || this.stance==='Soporte Implícito';
			},
			showFakeNewsQuestion: function(){
				return this.stance==='Negación Explícita' || this.stance==='Negación Implícita';
			},
			showEvidenceQuestion: function(){
				return  (this.showTrueNewsQuestion || this.showFakeNewsQuestion) && this.evidence === 'Si';
			}
		},
		methods: {
			updateStance(value){
				this.stance = value;
			},
			updateEvidence(value){
				this.evidence = value;
			}
		},
		template: `
			<div>
				<button 
					class="btn btn-block alert-primary mt-2" 
					:data-target="'#'.concat(section.id)" 
					data-toggle="collapse"  
					type="button" role="button" aria-expanded="false"
				>
					<h6>#[[ section.name ]]</h6>
				</button>					                                                                             	
				<div class="collapse mb-2" :id="section.id">
					<div class="card card-body">
						<template v-for="question in section.questions">
							<question-block-target-tweet-country
							:question='question'
							:options='question.options'
							v-if ='question.id == 1'
							>
							</question-block-target-tweet-country>

							<question-block-stance-of-response-to-target-content
							:question='question'
							:options='question.options'
							@stancechanged="updateStance"
							v-else-if ='question.id == 7'
							>
							</question-block-stance-of-response-to-target-content>
							
							<question-block-true-news
							:question='question'
							:options='question.options'
							:show = 'showTrueNewsQuestion'
							@evidencechanged="updateEvidence"
							v-else-if ="question.id == 9 "
							>
							</question-block-true-news>
						
							<question-block-fake-news
							:question='question'
							:options='question.options'
							:show = 'showFakeNewsQuestion'																							
							@evidencechanged="updateEvidence"
							v-else-if ="question.id == 10 "
							>
							</question-block-fake-news>

							<question-block
							:question='question'
							:options='question.options'												
							:show = 'showEvidenceQuestion'
							v-else-if ="question.id == 11 "
							>
							</question-block>

							<question-block
							:question='question'
							:options='question.options'
							v-else
							>
							</question-block>
						</template>
					</div>
				</div>
			</div>
		`
	})

	const store = new Vuex.Store({
		state: {
			tweetRelationId: document.getElementById('tweet_relation_id').value,
			showPreviousAnswers: document.getElementById('showPreviousAnswers').dataset.value.toLowerCase() == "true"
		},
	})

	//Vue app
	var annotationApp = new Vue({
		el: '#annotationApp',		
		delimiters: ['#[[', ']]'],
		data() {
			return {
				sections: [],
				tweetRelation : null,
			}			
		},
		computed: {
		},
		methods : {
			fetchSections(){
				fetch('/api/questions/grouped_by_section')	
					.then(stream => stream.json())
					.then((data) => this.sections = data)
					.then(() => console.log(this.sections))
					.catch(error => console.error(error))
			},
		},
		mounted(){
			this.fetchSections()
		},		
		store: store,
	})

	});
