$(document).ready(function() {
	function renderTweet(divId, tweetOptions){
		// https://developer.twitter.com/en/docs/twitter-for-websites/javascript-api/guides/scripting-factory-functions		console.log(document.getElementById(divId))
		twttr.widgets.createTweet(
			document.getElementById(divId).dataset.tweetId,
			document.getElementById(divId),
			tweetOptions
		)
		.then(function(el){
			// Hides tweet card inside target tweet in Quote
			$(el.shadowRoot).find(".Tweet-card").hide();
		})
		.catch(function(err){
			//Enter here when can't render the tweet because it has been deleted
			document.getElementById(divId).textContent = document.getElementById(divId).dataset.tweetText;
		});

	}
	//Render tweets
	twttr.ready(function() {
		let tweetOptions = { align: "center", width: "325", dnt: true, conversation: "none"}

		renderTweet('tweetTarget', tweetOptions);
		renderTweet('tweetResponse', tweetOptions);
	});	


	/*twttr.ready(function (twttr) {		
	 $(".tweet-box").each(renderTweet);
	});*/
	
	//Logic to handle dynamic changes of the form based on the stance selected
	$("input[name='stance']").click(function(event){
		positiveStance = event.target.value === "Explicit Support" || event.target.value === "Implicit Support";
		negativeStance = event.target.value === "Explicit Denial"  || event.target.value === "Implicit Denial";
		if( positiveStance ){
			showExpressivityForm();
			makeExpressivityFormRequired();

			document.querySelector("p#expressivity_label").textContent = 'verdadera o correcta';
			document.querySelector("input[name='expressivity_type']").value = 'True News';
		} else if ( negativeStance ){
			showExpressivityForm();			
			makeExpressivityFormRequired();

			document.querySelector("p#expressivity_label").textContent = 'falsa o incorrecta';
			document.querySelector("input[name='expressivity_type']").value = 'Fake News';
		} else {
			hideExpressivityForm();
			makeExpressivityFormNonRequired();

			document.querySelector("input[name='expressivity_type']").value = '';
		}

		function showExpressivityForm(){
			document.querySelector("div#expressivity_form").style.display = 'block';
		}

		function hideExpressivityForm(){
			document.querySelector("div#expressivity_form").style.display = 'none';
		}

		function makeExpressivityFormRequired(){
			document.querySelector("input[name='expressivity_value']").required = true;			
			document.querySelector("input[name='evidence']").required = true;
		}

		function makeExpressivityFormNonRequired(){
			document.querySelector("input[name='expressivity_value']").required = false;			
			document.querySelector("input[name='evidence']").required = false;
		}

	});


	//Vue app
	var annotationApp = new Vue({
		el: '#annotationApp',		
		delimiters: ['#[[', ']]'],
		data() {
			return {		  		
				questions : null,
				questionsGrouped : null,
				tweetRelation : null,				
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
