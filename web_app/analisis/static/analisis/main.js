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
		if(checkedOne){
			var time_spent = dateDiffInSecond(START_TIME, new Date());
			addFieldsToForm('time_spent',time_spent);			
			$("#mainFormSubmitButton").attr('disabled', true);
			return true
		}else{
			alert('Debe seleccionar al menos una opcion. En preguntas de opción múltiple.')			
			return false
		}

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
			<h6> #[[ question.value ]] </h6>
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
			<h6> #[[ question.value ]] </h6>
			<ul class="list-unstyled card-columns">
				<li class="form-check" v-for="option in options">
					<input 
						class="form-check-input"
						type="radio"
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

	//Vue app
	var annotationApp = new Vue({
		el: '#annotationApp',		
		delimiters: ['#[[', ']]'],
		data() {
			return {
				questions : null,
				questionsGrouped : null,
				tweetRelation : null,
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
		methods : {
			fetchQuestions(){
				fetch('/api/questions')
					.then(stream => stream.json())
					.then(function(data){
						data.forEach(q => q.options = JSON.parse(q.options))
						return data
					})
					.then((data) => {
						this.questions = data
						this.questionsGrouped = this.groupBySection(data)
						return data
					})
					.then(() => console.log(this.questions))
                    .catch(error => console.error(error))
			},
			groupBySection(questions){
				const bySection = R.groupBy(q => q.section)
				return bySection(questions)
			},
			idFromSentence(sectionName){
				const copy = sectionName
				return copy.replace(/[^0-9a-zA-Z-]/g, '').toLowerCase()
			},
			updateStance(value){
				this.stance = value;
			},
			updateEvidence(value){
				this.evidence = value;
			}
		},
		mounted(){
			this.fetchQuestions()
		}
	})

	});
