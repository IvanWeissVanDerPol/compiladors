import json
import re
from utils import log_message

class Tokenizer:
    def __init__(self, positive_words, negative_words, neutral_words):
        log_message("Tokenizer.__init__ called")
        self.positive_words = positive_words
        self.negative_words = negative_words
        self.neutral_words = neutral_words
        # log_message(f"Tokenizer initialized with positive_words={positive_words}, negative_words={negative_words}, neutral_words={neutral_words}")

    @classmethod
    def from_json(cls, json_file_path):
        log_message("Tokenizer.from_json called")
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            # log_message(f"Loaded data from {json_file_path}: {data}")
        return cls(
            positive_words=data['BUENAS'],
            negative_words=data['MALAS'],
            neutral_words=data['NEUTRAS']
        )

    def normalize_word(self, original_word):
        # log_message(f"Tokenizer.normalize_word called with original_word={original_word}")
        # Normalize word to handle number and gender variations
        updated_word = original_word.lower()
        # log_message(f"Word converted to lowercase: {updated_word}")
        if updated_word.isdigit():
            # log_message("Word is a digit, returning 'neutral_number'")
            return 'neutral_number'  # Special token for numbers
        if updated_word.endswith('s'):
            updated_word = updated_word[:-1]  # Remove plural 's'
            # log_message(f"Removed plural 's': {updated_word}")
        if updated_word.endswith('a'):
            updated_word = updated_word[:-1] + 'o'  # Convert feminine to masculine
            # log_message(f"Converted feminine to masculine: {updated_word}")
        return updated_word

    def tokenize(self, text):
        log_message(f"Tokenizer.tokenize called with text={text}")
        # Improved tokenization to handle punctuation and special characters
        tokens = re.findall(r'\b\w+\b', text.lower())
        log_message(f"Tokenized text into tokens: {tokens}")
        normalized_tokens = [(token, self.normalize_word(token)) for token in tokens]
        log_message(f"Normalized tokens: {normalized_tokens}")
        return normalized_tokens

    def evaluate(self, tokens):
        log_message(f"Tokenizer.evaluate called with tokens={tokens}")
        positive_count = sum(1 for token in tokens if token in self.positive_words)
        negative_count = sum(1 for token in tokens if token in self.negative_words)
        neutral_count = sum(1 for token in tokens if token in self.neutral_words)
        log_message(f"Evaluation results - positive: {positive_count}, negative: {negative_count}, neutral: {neutral_count}")
        
        return {
            'positive': positive_count,
            'negative': negative_count,
            'neutral': neutral_count
        }

    def evaluate_performance(self, conversation):
        log_message("Tokenizer.evaluate_performance called")
        criteria = {
            "greeting": ["Buenas noches","¿Cómo está?","¿Cómo le va?","¡Bienvenido!","¡Bienvenida!","¿En qué puedo ayudarle?","¿Cómo puedo asistirte?","Hola, ¿cómo estás?","Hola, ¿qué tal?","¡Hola, bienvenido!","¡Hola, bienvenida!","¿Qué tal su día?","¿Qué tal su mañana?","¿Qué tal su tarde?","¡Buenos días, bienvenido!","¡Buenas tardes, bienvenida!","¡Buenos días, señor!","¡Buenas tardes, señora!","¡Buenas noches, señor!","¡Buenas noches, señora!","Hola, ¿cómo le puedo ayudar?","Hola, ¿cómo le va hoy?","Hola, ¿qué tal su día?","¡Hola, qué gusto verlo!","¡Hola, qué gusto verla!","¿Cómo amaneció?","¿Cómo anocheció?","¿En qué puedo servirle hoy?","¿Cómo puedo asistirte hoy?","¡Hola, bienvenido de nuevo!","¡Hola, bienvenida de nuevo!","¿Cómo ha estado?","¿Cómo ha sido su día?","¡Hola, qué alegría verlo!","¡Hola, qué alegría verla!","¡Qué gusto tenerlo aquí!","¡Qué gusto tenerla aquí!","Hola, ¿cómo está usted?","¡Hola, buenos días!","¡Hola, buenas tardes!","¡Hola, buenas noches!","Hola, ¿qué puedo hacer por usted?","Hola, ¿cómo ha estado?","¡Hola, qué placer verlo!","¡Hola, qué placer verla!","Hola, ¿cómo le ha ido?","Hola, ¿cómo le ha estado yendo?","¡Hola, bienvenido a nuestro servicio!","¡Hola, bienvenida a nuestro servicio!","Hola, ¿qué tal ha sido su experiencia?",],
            "ask_number": ["número de teléfono","número de cuenta","número de pedido","número de referencia","número de identificación","número de transacción","número de tarjeta","número de factura","número de seguro social","número de tarjeta de crédito","número de reserva","número de confirmación","número de serie","número de membresía","número de póliza","número de seguimiento","número de recibo","número de inscripción","número de registro","número de contrato"],
            "provide_info": ["detalle","balance","información","detalles","estado","disponible","transacciones","última operación","historial","datos","documentos","actualización","movimientos","cobertura","informes","extracto","registro","comprobante","notificación","alerta"],
            "offer_assistance": ["puedo ayudarle","necesita ayuda","puedo asistirte","puedo hacer algo más","algo más que pueda hacer","requiere asistencia","alguna otra cosa","algo adicional","otra cosa","puedo ofrecerle algo más","puedo asistirlo en algo más","alguna otra ayuda","necesita otra cosa","algo más que pueda necesitar","puedo ayudar con algo más","hay algo más","algo más que necesite","necesita algo adicional","puedo ofrecer más ayuda","hay algo más que desee"],
            "end_politely": ["hasta pronto","nos vemos","que tenga buen día","que tenga buena tarde","que tenga buena noche","que pase bien","cuídese","le agradezco","gracias por su tiempo","muchas gracias","fue un placer","hasta la próxima","le deseo lo mejor","hasta mañana","adiós","quedamos a su disposición","quedamos a sus órdenes","gracias por contactarnos","que tenga un excelente día","saludos cordiales"]
        }
        
        performance_score = 0
        for key, phrases in criteria.items():
            if any(phrase in conversation.lower() for phrase in phrases):
                performance_score += 1
                log_message(f"Criteria '{key}' met")
        
        log_message(f"Performance score: {performance_score}/{len(criteria)}")
        return performance_score

    def evaluate_experience(self, conversation):
        log_message("Tokenizer.evaluate_experience called")
        tokens = self.tokenize(conversation)
        positive_count = sum(1 for _, normalized_word in tokens if normalized_word in self.positive_words)
        negative_count = sum(1 for _, normalized_word in tokens if normalized_word in self.negative_words)
        neutral_count = sum(1 for _, normalized_word in tokens if normalized_word in self.neutral_words)
        
        experience_score = positive_count - negative_count
        log_message(f"Experience score: {experience_score} (positive: {positive_count}, negative: {negative_count}, neutral: {neutral_count})")
        
        return {
            "positive": positive_count,
            "negative": negative_count,
            "neutral": neutral_count,
            "score": experience_score
        }
