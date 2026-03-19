{{/*
Expand the name of the chart.
*/}}
{{- define "lagnamaster.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "lagnamaster.labels" -}}
helm.sh/chart: {{ .Chart.Name }}-{{ .Chart.Version }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Image reference helper
*/}}
{{- define "lagnamaster.image" -}}
{{ .Values.image.registry }}/{{ .Values.image.owner }}/{{ .name }}:{{ .Values.image.tag }}
{{- end }}

{{/*
Secret env vars shared by api, ui, worker
*/}}
{{- define "lagnamaster.secretEnv" -}}
- name: JWT_SECRET
  valueFrom:
    secretKeyRef:
      name: {{ .Values.secrets.existingSecret }}
      key: JWT_SECRET
- name: PG_DSN
  valueFrom:
    secretKeyRef:
      name: {{ .Values.secrets.existingSecret }}
      key: PG_DSN
- name: REDIS_URL
  valueFrom:
    secretKeyRef:
      name: {{ .Values.secrets.existingSecret }}
      key: REDIS_URL
{{- end }}

{{/*
Common env vars from values
*/}}
{{- define "lagnamaster.commonEnv" -}}
- name: JWT_ALGORITHM
  value: {{ .Values.env.JWT_ALGORITHM | quote }}
- name: ACCESS_TTL_MIN
  value: {{ .Values.env.ACCESS_TTL_MIN | quote }}
- name: REFRESH_TTL_DAY
  value: {{ .Values.env.REFRESH_TTL_DAY | quote }}
- name: CACHE_VERSION
  value: {{ .Values.env.CACHE_VERSION | quote }}
- name: PG_POOL_MIN
  value: {{ .Values.env.PG_POOL_MIN | quote }}
- name: PG_POOL_MAX
  value: {{ .Values.env.PG_POOL_MAX | quote }}
{{- end }}
