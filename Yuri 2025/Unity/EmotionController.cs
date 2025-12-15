using System.Collections;
using System.Collections.Generic;
using Live2D.Cubism.Core;
using Live2D.Cubism.Framework.Motion;
using Live2D.Cubism.Framework.Physics;
using UnityEngine;

public class EmotionController : MonoBehaviour
{
   Animator myAnimator;

   tcpTest mytcpTest;

   Coroutine currentRoutine;
   const string playCurious_ANIM = "playCurious";
   const string playHappy_ANIM = "playHappy";
   const string playCry_ANIM = "playCry";
   const string playShame_ANIM = "playShame";
   const string playShock_ANIM = "playShock";
   const string playTundere_ANIM = "playTundere";
   const string playTalking_ANIM = "playTalking";
   void Start ()
   {
        myAnimator = GetComponent<Animator>();
        mytcpTest = GetComponent<tcpTest>();
    
   }

    //Debug.Log("進去了嗎 -->" + mytcpTest.needCurious);  
    public void PlayAnimation(string emotion, float duration)
    {
        if (currentRoutine != null)
            StopCoroutine(currentRoutine);

        currentRoutine = StartCoroutine(
            PlayAnimationCoroutine(emotion, duration)
        );
    } 

    IEnumerator PlayAnimationCoroutine(string emotion, float duration)
    {
        // clear trigger first to prevent animation crash to each other
        myAnimator.ResetTrigger(playCurious_ANIM);
        myAnimator.ResetTrigger(playHappy_ANIM);
        myAnimator.ResetTrigger(playCry_ANIM);
        myAnimator.ResetTrigger(playShame_ANIM);
        myAnimator.ResetTrigger(playShock_ANIM);
        myAnimator.ResetTrigger(playTundere_ANIM);
        myAnimator.ResetTrigger(playTalking_ANIM);
        Debug.Log($"動畫: {emotion}, 時長: {duration}");
        // activate anmiation
        switch (emotion)
        {
            case "Interested": myAnimator.SetTrigger(playCurious_ANIM); break;
            case "Happy": myAnimator.SetTrigger(playHappy_ANIM); break;
            case "Sad": myAnimator.SetTrigger(playCry_ANIM); break;
            case "Sensitive": myAnimator.SetTrigger(playShame_ANIM); break;
            case "Surprised": myAnimator.SetTrigger(playShock_ANIM); break;
            case "Bad": myAnimator.SetTrigger(playTundere_ANIM); break;
            case "Neutral": myAnimator.SetTrigger(playTalking_ANIM); break;
        }

        // animation time = tts mp3 time
        yield return new WaitForSeconds(duration);
    }
   public void setCurious()
   {
        if(mytcpTest.needCurious == true)
        {    
          myAnimator.SetTrigger(playCurious_ANIM);
          mytcpTest.resetvalues();
          Debug.Log("needCurious==False??-->" + mytcpTest.needCurious);
        }
   }
      public void setHappy()
   {
        if(mytcpTest.needHappy == true)
        {    
          myAnimator.SetTrigger(playHappy_ANIM);
          mytcpTest.resetvalues();
          Debug.Log("needHappy==False??-->" + mytcpTest.needHappy);
        }
   }
      public void setCry()
   {
        if(mytcpTest.needCry == true)
        {    
          myAnimator.SetTrigger(playCry_ANIM);
          mytcpTest.resetvalues();
          Debug.Log("needCry==False??-->" + mytcpTest.needCry);
        }
   }
      public void setShame()
   {
        if(mytcpTest.needShame == true)
        {    
          myAnimator.SetTrigger(playShame_ANIM);
          mytcpTest.resetvalues();
          Debug.Log("needShame==False??-->" + mytcpTest.needShame);
        }
   }
      public void setShock()
   {
        if(mytcpTest.needShock == true)
        {    
          myAnimator.SetTrigger(playShock_ANIM);
          mytcpTest.resetvalues();
          Debug.Log("needShock==False??-->" + mytcpTest.needShock);
        }
   }
      public void setTundere()
   {
        if(mytcpTest.needTundere == true)
        {    
          myAnimator.SetTrigger(playTundere_ANIM);
          mytcpTest.resetvalues();
          Debug.Log("needTundere==False??-->" + mytcpTest.needTundere);
        }
   }
      public void setTalking()
   {
        if(mytcpTest.needTalking == true)
        {    
          myAnimator.SetTrigger(playTalking_ANIM);
          mytcpTest.resetvalues();
          Debug.Log("needTalking==False??-->" + mytcpTest.needTalking);
        }
   }

   private void Update()
    {
        
    }
}
