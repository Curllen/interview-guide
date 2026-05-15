# Graphify Analysis Report

## Overview
- **Nodes**: 2352
- **Edges**: 5451
- **Communities**: 59
- **Files Analyzed**: 329

## Key Nodes
1. **.get()** (score: 0.047)
   - Source: app/src/main/java/interview/guide/infrastructure/redis/RedisService.java
2. **.error()** (score: 0.046)
   - Source: app/src/main/java/interview/guide/common/result/Result.java
3. **list** (score: 0.031)
4. **.success()** (score: 0.031)
   - Source: app/src/main/java/interview/guide/common/result/Result.java
5. **slf4j** (score: 0.026)
6. **.findById()** (score: 0.024)
   - Source: app/src/main/java/interview/guide/modules/resume/service/ResumePersistenceService.java
7. **VoiceInterviewWebSocketHandler** (score: 0.023)
   - Source: app/src/main/java/interview/guide/modules/voiceinterview/handler/VoiceInterviewWebSocketHandler.java
8. **LlmProviderConfigService** (score: 0.023)
   - Source: app/src/main/java/interview/guide/modules/llmprovider/service/LlmProviderConfigService.java
9. **InterviewSessionEntity** (score: 0.022)
   - Source: app/src/main/java/interview/guide/modules/interview/model/InterviewSessionEntity.java
10. **LlmProviderConfigService.java** (score: 0.021)
   - Source: app/src/main/java/interview/guide/modules/llmprovider/service/LlmProviderConfigService.java

## Communities
### 1. Resume Analysis Module (size: 523, cohesion: 0.011)
   - list (degree: 64)
   - slf4j (degree: 58)
   - LlmProviderConfigService.java (degree: 44)
   - service (degree: 41)
   - BusinessException (degree: 39)

### 2. Resume Analysis Module (size: 339, cohesion: 0.015)
   - .error() (degree: 60)
   - .get() (degree: 59)
   - VoiceInterviewWebSocketHandler (degree: 52)
   - InterviewSessionEntity (degree: 47)
   - InterviewAnswerEntity (degree: 29)

### 3. Resume Analysis Module (size: 180, cohesion: 0.015)
   - ResumeEntity (degree: 37)
   - ResumeAnalysisEntity (degree: 30)
   - AnalyzeStreamConsumer (degree: 14)
   - ResumeMapper (degree: 11)
   - InterviewSessionRepository (degree: 11)

### 4. Knowledge Base & RAG (size: 170, cohesion: 0.021)
   - InterviewSkillService (degree: 30)
   - RedisService (degree: 30)
   - InterviewQuestionService (degree: 18)
   - BusinessException (degree: 17)
   - UnifiedEvaluationService (degree: 16)

### 5. Knowledge Base & RAG (size: 168, cohesion: 0.016)
   - KnowledgeBaseEntity (degree: 44)
   - KnowledgeBaseRepository (degree: 20)
   - KnowledgeBaseListService (degree: 13)
   - VectorizeStreamConsumer (degree: 13)
   - RagChatSessionService (degree: 12)

### 6. Resume Analysis Module (size: 149, cohesion: 0.022)
   - data (degree: 31)
   - builder (degree: 17)
   - noargsconstructor (degree: 16)
   - allargsconstructor (degree: 16)
   - VoiceInterviewProperties.java (degree: 13)

### 7. Resume Analysis Module (size: 125, cohesion: 0.041)
   - LlmProviderConfigService (degree: 48)
   - LlmProviderRegistry (degree: 25)
   - .findById() (degree: 15)
   - .getEmbeddingModel() (degree: 14)
   - .trimOrNull() (degree: 12)

### 8. Interview Scheduling & Management (size: 117, cohesion: 0.030)
   - VoiceInterviewService (degree: 30)
   - .getCurrentPhase() (degree: 15)
   - .shouldTransitionToNextPhase() (degree: 12)
   - workspace_app_src_main_java_interview_guide_modules_voiceinterview_service_voiceinterviewservice_java (degree: 11)
   - VoiceEvaluateStreamProducer (degree: 9)

### 9. Resume Analysis Module (size: 85, cohesion: 0.041)
   - .success() (degree: 70)
   - LlmProviderController (degree: 15)
   - KnowledgeBaseController (degree: 13)
   - InterviewController (degree: 12)
   - VoiceInterviewController (degree: 9)

### 10. Core Services Layer (size: 58, cohesion: 0.054)
   - .cleanText() (degree: 20)
   - DocumentParseServiceTest (degree: 14)
   - CleanTextTests (degree: 13)
   - TextCleaningServiceTest.java (degree: 8)
   - .stripHtml() (degree: 8)

### 11. Voiceinterview Module (size: 48, cohesion: 0.049)
   - WebSocketConfig.java (degree: 10)
   - S3Config.java (degree: 8)
   - bean (degree: 7)
   - configuration (degree: 7)
   - LlmEmbeddingConfig.java (degree: 6)

### 12. Knowledge Base & RAG (size: 39, cohesion: 0.105)
   - .similaritySearch() (degree: 16)
   - .vectorizeAndStore() (degree: 11)
   - SimilaritySearchTests (degree: 9)
   - .createMockDocuments() (degree: 9)
   - KnowledgeBaseVectorService (degree: 7)

### 13. Core Services Layer (size: 36, cohesion: 0.097)
   - AbstractStreamConsumer (degree: 22)
   - .processMessage() (degree: 12)
   - RateLimitIntegrationTest (degree: 6)
   - .ackMessage() (degree: 5)
   - .startConsumer() (degree: 5)

### 14. Test Suite (size: 30, cohesion: 0.083)
   - StripTrailingSlashes (degree: 13)
   - .baseUrlContainsVersion() (degree: 9)
   - ContainsVersion (degree: 7)
   - BuildOpenAiApi (degree: 7)
   - ApiPathResolver (degree: 5)

### 15. Llmprovider Module (size: 28, cohesion: 0.103)
   - .createProviderConfig() (degree: 7)
   - EnvFileOperations (degree: 6)
   - .createServiceWithEnv() (degree: 5)
   - ProviderManagement (degree: 5)
   - .invokeMethod() (degree: 5)

### 16. Voiceinterview Module (size: 26, cohesion: 0.114)
   - QwenTtsService (degree: 16)
   - QwenTtsServiceTest (degree: 8)
   - .testReloadUpdatesAllFields() (degree: 7)
   - .setUp() (degree: 6)
   - .setMode() (degree: 3)

### 17. Knowledge Base & RAG (size: 24, cohesion: 0.185)
   - KnowledgeBaseQueryService (degree: 18)
   - .answerQuestionStream() (degree: 12)
   - .answerQuestion() (degree: 11)
   - .buildQueryContext() (degree: 6)
   - .normalizeStreamOutput() (degree: 4)

### 18. Core Services Layer (size: 17, cohesion: 0.176)
   - InterviewScheduleService (degree: 8)
   - .toDTO() (degree: 5)
   - InterviewScheduleRepository (degree: 5)
   - .getByIdOrThrow() (degree: 4)
   - .getAll() (degree: 3)

### 19. Interview Scheduling & Management (size: 14, cohesion: 0.187)
   - EvaluateStreamConsumer (degree: 13)
   - .updateEvaluateStatus() (degree: 5)
   - .retryMessage() (degree: 2)
   - .markFailed() (degree: 2)
   - .markCompleted() (degree: 2)

### 20. Voiceinterview Module (size: 13, cohesion: 0.154)
   - VoiceEvaluateStreamConsumer (degree: 12)
   - .threadName() (degree: 1)
   - .markCompleted() (degree: 1)
   - .VoiceEvaluateStreamConsumer() (degree: 1)
   - .groupName() (degree: 1)

### 21. Component Group 21 (size: 12, cohesion: 0.167)
   - App.java (degree: 10)
   - App (degree: 2)
   - springapplication (degree: 1)
   - enablescheduling (degree: 1)
   - openaimoderationautoconfiguration (degree: 1)

### 22. Component Group 22 (size: 12, cohesion: 0.167)
   - GlobalExceptionHandler.java (degree: 11)
   - restcontrolleradvice (degree: 1)
   - maxuploadsizeexceededexception (degree: 1)
   - fielderror (degree: 1)
   - resourceaccessexception (degree: 1)

### 23. Core Services Layer (size: 10, cohesion: 0.467)
   - InterviewParseService (degree: 9)
   - .tryRuleParsing() (degree: 6)
   - .parse() (degree: 6)
   - .parseDateTime() (degree: 5)
   - .parseFeishu() (degree: 4)

### 24. Test Suite (size: 10, cohesion: 0.200)
   - DocumentParseIntegrationTest (degree: 9)
   - .testEmptyContentHandling() (degree: 1)
   - .testTextCleaningIntegration() (degree: 1)
   - .testNoiseOnlyDocument() (degree: 1)
   - .testParseTextWithSpecialCharacters() (degree: 1)

### 25. Common Utilities (size: 10, cohesion: 0.200)
   - CommonConstants.java (degree: 4)
   - CommonConstants (degree: 3)
   - Pagination (degree: 2)
   - InterviewDefaults (degree: 2)
   - StatusCode (degree: 2)

### 26. Test Suite (size: 8, cohesion: 0.250)
   - LlmProviderRegistryTest (degree: 7)
   - .testReload() (degree: 1)
   - .testGetChatClient_UnknownProvider() (degree: 1)
   - .setUp() (degree: 1)
   - .testGetChatClient_disabledProvider() (degree: 1)

### 27. Core Services Layer (size: 7, cohesion: 0.286)
   - ContentTypeDetectionService (degree: 6)
   - .isPdf() (degree: 1)
   - .isPlainText() (degree: 1)
   - .ContentTypeDetectionService() (degree: 1)
   - .detectContentType() (degree: 1)

### 28. Test Suite (size: 7, cohesion: 0.429)
   - LlmProviderRegistryPathIntegrationTest (degree: 6)
   - .buildRegistryFor() (degree: 4)
   - .baseUrlWithoutVersion_defaultPath() (degree: 2)
   - .baseUrlWithV3_noDoubleVersion() (degree: 2)
   - .baseUrlWithV1_noDoubleVersion() (degree: 2)

### 29. Component Group 29 (size: 7, cohesion: 0.333)
   - NoOpEmbeddedDocumentExtractor.java (degree: 4)
   - NoOpEmbeddedDocumentExtractor (degree: 4)
   - EmbeddedDocumentExtractor (degree: 2)
   - .parseEmbedded() (degree: 1)
   - contenthandler (degree: 1)

### 30. Component Group 30 (size: 7, cohesion: 0.286)
   - RateLimit.java (degree: 6)
   - ratelimitaspect (degree: 1)
   - retentionpolicy (degree: 1)
   - elementtype (degree: 1)
   - retention (degree: 1)

### 31. Test Suite (size: 6, cohesion: 0.333)
   - RateLimitExceededExceptionTest (degree: 5)
   - .testDefaultConstructor() (degree: 1)
   - .testInheritance() (degree: 1)
   - .testMessageWithCauseConstructor() (degree: 1)
   - .testMessageConstructor() (degree: 1)

### 32. Test Suite (size: 5, cohesion: 0.400)
   - RateLimitScriptTest (degree: 4)
   - .testAnnotationMetadata() (degree: 1)
   - .testCustomValues() (degree: 1)
   - .testDefaultValues() (degree: 1)
   - .testRepeatableAnnotations() (degree: 1)

### 33. Component Group 33 (size: 5, cohesion: 0.400)
   - GetChatClientOrDefault (degree: 7)
   - .blankProviderFallsBackToDefault() (degree: 2)
   - .nullProviderFallsBackToDefault() (degree: 2)
   - .explicitProvider() (degree: 2)
   - .setUpProviders() (degree: 1)

### 34. Knowledge Base & RAG (size: 4, cohesion: 0.500)
   - KnowledgeBaseParseService (degree: 3)
   - .downloadAndParseContent() (degree: 1)
   - .parseContent() (degree: 1)
   - .detectContentType() (degree: 1)

### 35. Test Suite (size: 4, cohesion: 0.500)
   - AppTest.java (degree: 2)
   - AppTest (degree: 2)
   - .contextLoads() (degree: 1)
   - assertnotnull (degree: 1)

### 36. Llmprovider Module (size: 4, cohesion: 0.500)
   - YamlMutations (degree: 3)
   - .nullYamlPathIsNoOp() (degree: 1)
   - .createsNewFileWhenMissing() (degree: 1)
   - .preservesExistingStructure() (degree: 1)

### 37. Voiceinterview Module (size: 4, cohesion: 0.500)
   - ErrorHandlingTests (degree: 3)
   - .testEmptyConfiguration() (degree: 1)
   - .testInvalidSessionId() (degree: 1)
   - .testDifferentRoleTypes() (degree: 1)

### 38. Voiceinterview Module (size: 4, cohesion: 0.500)
   - ConfigurationTests (degree: 3)
   - .testPhaseConfiguration() (degree: 1)
   - .testPhaseConfigParameters() (degree: 1)
   - .testConfigurationCompleteness() (degree: 1)

### 39. Voiceinterview Module (size: 4, cohesion: 0.500)
   - VoiceInterviewSessionStatusTest (degree: 3)
   - .shouldHaveFourStatuses() (degree: 1)
   - VoiceInterviewSessionStatusTest.java (degree: 1)
   - .shouldHaveExpectedStatusNames() (degree: 1)

### 40. Knowledge Base & RAG (size: 4, cohesion: 0.500)
   - DeleteVectorDataTests (degree: 3)
   - .testDeleteByKnowledgeBaseId() (degree: 1)
   - .testDeleteNonExistentKnowledgeBase() (degree: 1)
   - .testDeleteFailureSilentlyHandled() (degree: 1)

### 41. Test Suite (size: 4, cohesion: 0.500)
   - TestClass (degree: 3)
   - .customMethod() (degree: 1)
   - .defaultMethod() (degree: 1)
   - .multiRuleMethod() (degree: 1)

### 42. Component Group 42 (size: 4, cohesion: 0.500)
   - RateLimitExceededException (degree: 3)
   - workspace_app_src_main_java_interview_guide_common_aspect_ratelimitaspect_java (degree: 1)
   - RateLimitExceededException.java (degree: 1)
   - .RateLimitExceededException() (degree: 1)

### 43. Voiceinterview Module (size: 3, cohesion: 0.667)
   - VoiceInterviewIntegrationTest (degree: 2)
   - .setUp() (degree: 1)
   - .tearDown() (degree: 1)

### 44. Llmprovider Module (size: 2, cohesion: 1.000)
   - DefaultProviderDTO() (degree: 1)
   - DefaultProviderDTO.java (degree: 1)

### 45. Llmprovider Module (size: 2, cohesion: 1.000)
   - UpdateProviderRequest() (degree: 1)
   - UpdateProviderRequest.java (degree: 1)

### 46. Build Configuration (size: 1, cohesion: 1.000)
   - settings.gradle (degree: 0)

### 47. Build Configuration (size: 1, cohesion: 1.000)
   - build.gradle (degree: 0)

### 48. Component Group 48 (size: 1, cohesion: 1.000)
   - InterviewStatus.java (degree: 0)

### 49. Llmprovider Module (size: 1, cohesion: 1.000)
   - AsrConfigRequest.java (degree: 0)

### 50. Llmprovider Module (size: 1, cohesion: 1.000)
   - TtsConfigRequest.java (degree: 0)

### 51. Voiceinterview Module (size: 1, cohesion: 1.000)
   - VoiceInterviewSessionStatus.java (degree: 0)

### 52. Interview Scheduling & Management (size: 1, cohesion: 1.000)
   - SubmitAnswerResponse.java (degree: 0)

### 53. Interview Scheduling & Management (size: 1, cohesion: 1.000)
   - HistoricalQuestion.java (degree: 0)

### 54. Knowledge Base & RAG (size: 1, cohesion: 1.000)
   - KnowledgeBaseStatsDTO.java (degree: 0)

### 55. Knowledge Base & RAG (size: 1, cohesion: 1.000)
   - QueryResponse.java (degree: 0)

### 56. Knowledge Base & RAG (size: 1, cohesion: 1.000)
   - VectorStatus.java (degree: 0)

### 57. Component Group 57 (size: 1, cohesion: 1.000)
   - QaRecord.java (degree: 0)

### 58. Component Group 58 (size: 1, cohesion: 1.000)
   - AsyncTaskStatus.java (degree: 0)

### 59. Component Group 59 (size: 1, cohesion: 1.000)
   - rate_limit_single.lua (degree: 0)
