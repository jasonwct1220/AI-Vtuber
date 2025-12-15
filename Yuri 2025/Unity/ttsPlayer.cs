using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;

public class ttsPlayer : MonoBehaviour
{
    public EmotionController emotionController;
    // Start is called before the first frame update
    void Start()
    {
        
    }

    public AudioSource audioSource;
    public Animator myAnimator;

    Coroutine currentRoutine;

    public void PlayTTS(string emotion, string mp3Path)
    {
        Debug.Log($"[TTSPlayer] mp3Path={mp3Path}, emotion={emotion}");
        if (currentRoutine != null)
            StopCoroutine(currentRoutine);

        currentRoutine = StartCoroutine(
            PlayTTSRoutine(emotion, mp3Path)
        );
    }

    IEnumerator PlayTTSRoutine(string emotion, string mp3Path)
    {
        yield return StartCoroutine(LoadAndPlayMp3(mp3Path));

        float duration = audioSource.clip.length;

        emotionController.PlayAnimation(emotion, duration);
    }

    IEnumerator LoadAndPlayMp3(string filePath)
    {
        string url = "file://" + filePath;

        using (UnityWebRequest www =
            UnityWebRequestMultimedia.GetAudioClip(url, AudioType.MPEG))
        {
            yield return www.SendWebRequest();

            if (www.result != UnityWebRequest.Result.Success)
            {
                Debug.LogError(www.error);
                yield break;
            }

            audioSource.clip = DownloadHandlerAudioClip.GetContent(www);
            audioSource.Play();
        }
    }
    // Update is called once per frame
    void Update()
    {
        
    }

    void Awake()
    {
        Debug.Log($"[ttsPlayer] Awake, instanceID = {GetInstanceID()}");
    
        if (emotionController == null)
        {
            emotionController = FindObjectOfType<EmotionController>();
            Debug.Log("[ttsPlayer] Auto bind EmotionController: " + emotionController);
        }

        if (emotionController == null)
        {
            Debug.LogError("Scene 裡找不到 emotionController");
        }
    
    }

    void OnDestroy()
    {
        Debug.Log($"[ttsPlayer] DESTROYED, instanceID = {GetInstanceID()}");
    }
}
