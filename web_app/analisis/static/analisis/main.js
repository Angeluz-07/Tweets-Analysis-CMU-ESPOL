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
	//
	Vue.component('question-block', {
		props : ['question','options'],
		delimiters : ['#[[',']]'],
  		data: function () {
			return {
			count: 0,
			no_clear_selected: false,
			cols: 2
			}
		},
		methods : {
			check: function(e){
				if (e.target.value === 'No es claro' && e.target.checked === true){
					//console.log(e);
					//console.log(this.$el.querySelectorAll('input:not([value="No es claro"])'));
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
		computed: {
			columns () {
			  let columns = []
			  let mid = Math.ceil(this.options.length / this.cols)
			  for (let col = 0; col < this.cols; col++) {
				columns.push(this.options.slice(col * mid, col * mid + mid))
			  }
			  return columns
			}
		},
		template: `
		<div>
		<h6> #[[ question.value ]] </h6>
			<div class="container_">
				<div class="col_" v-for="options in columns">
					<div class="form-check-inline item-container_" v-for="option in options">
						<label class="form-check-label">
						<input 
							class="form-check-input"
							type="radio"
							:name="question.id"
							:value="option" 
							v-if="question.type==='Choice'"
							required>
						<input 
							class="form-check-input"
							type="checkbox"
							:name="question.id"
							:value="option"
							@change="check($event)"
							v-else>
							#[[ option ]]
						</label>
					</div>
				</div>
			</div>
		</div>
		`
	})
	//Vue app
	var annotationApp = new Vue({
		el: '#annotationApp',		
		delimiters: ['#[[', ']]'],
		data() {
			return {
				questions : null,
				questionsGrouped : null,
				tweetRelation : null,
				stance: null, //model for the last section of questions		
				evidence: null, 	
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
		},
		mounted(){
			this.fetchQuestions()
		}
	})

	});
