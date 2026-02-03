class Sale {
  final int id;
  final String date;
  final double amount;
  final String type;
  final String category;
  final String description;

  Sale({
    required this.id,
    required this.date,
    required this.amount,
    required this.type,
    required this.category,
    required this.description,
  });

  factory Sale.fromJson(Map<String, dynamic> json) {
    return Sale(
      id: json['id'] as int,
      date: json['date'] as String,
      amount: (json['amount'] as num).toDouble(),
      type: json['type'] as String,
      category: json['category'] as String? ?? 'general',
      description: json['description'] as String? ?? '',
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'date': date,
      'amount': amount,
      'type': type,
      'category': category,
      'description': description,
    };
  }

  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'date': date,
      'amount': amount,
      'type': type,
      'category': category,
      'description': description,
    };
  }

  factory Sale.fromMap(Map<String, dynamic> map) {
    return Sale(
      id: map['id'] as int,
      date: map['date'] as String,
      amount: (map['amount'] as num).toDouble(),
      type: map['type'] as String,
      category: map['category'] as String? ?? 'general',
      description: map['description'] as String? ?? '',
    );
  }

  @override
  String toString() {
    return 'Sale(id: $id, date: $date, amount: $amount, type: $type, category: $category, description: $description)';
  }
}
