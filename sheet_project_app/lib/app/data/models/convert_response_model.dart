class ConvertResponseModel {
  String? status;
  String? filename;
  String? midiPath;

  ConvertResponseModel({this.status, this.filename, this.midiPath});

  ConvertResponseModel.fromJson(Map<String, dynamic> json) {
    status = json['status'];
    filename = json['filename'];
    midiPath = json['midi_path'];
  }

  Map<String, dynamic> toJson() {
    return {
      'status': status,
      'filename': filename,
      'midi_path': midiPath,
    };
  }
}
