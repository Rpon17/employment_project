import 'package:flutter/material.dart';
import 'package:get/get.dart';
import '../controllers/home_controller.dart';

class HomeView extends GetView<HomeController> {
  const HomeView({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("🎵 Bass Sheet Generator")),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Obx(() => Column(
          children: [
            TextField(
              decoration: const InputDecoration(
                labelText: "YouTube URL",
                border: OutlineInputBorder(),
              ),
              onChanged: (v) => controller.youtubeUrl.value = v,
            ),
            const SizedBox(height: 10),
            TextField(
              decoration: const InputDecoration(
                labelText: "File name",
                border: OutlineInputBorder(),
              ),
              onChanged: (v) => controller.filename.value = v,
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: controller.isLoading.value ? null : controller.convert,
              child: controller.isLoading.value
                  ? const CircularProgressIndicator(color: Colors.white)
                  : const Text("Convert"),
            ),
            const SizedBox(height: 20),
            if (controller.result.value != null) ...[
              Text("✅ 변환 완료"),
              Text("파일명: ${controller.result.value!.filename}"),
              Text("MIDI 경로: ${controller.result.value!.midiPath}"),
            ]
          ],
        )),
      ),
    );
  }
}
