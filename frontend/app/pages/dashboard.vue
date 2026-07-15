<script setup lang="ts">
import type {
  ParkingApplicationCreatePayload,
  ParkingApplicationRead,
  ParkingApplicationUpdatePayload,
} from '~/types/application'

definePageMeta({
  middleware: 'auth',
})

const { currentUser, fetchCurrentUser } = useAuth()

const {
  applications,
  pending,
  errorMessage,
  loadMyApplications,
  createApplication,
  updateApplication,
} = useApplications()

const successMessage = ref<string | null>(null)
const editingApplication = ref<ParkingApplicationRead | null>(null)

await fetchCurrentUser()
await loadMyApplications()

async function submitCreateApplication(payload: ParkingApplicationCreatePayload) {
  successMessage.value = null

  try {
    await createApplication(payload)
    successMessage.value = 'Wniosek został utworzony.'
  } catch {
    // errorMessage jest ustawiany w useApplications()
  }
}

async function submitUpdateApplication(payload: ParkingApplicationUpdatePayload) {
  if (!editingApplication.value) {
    return
  }

  successMessage.value = null

  try {
    await updateApplication(editingApplication.value.id, payload)
    successMessage.value = 'Wniosek został zaktualizowany.'
    editingApplication.value = null
  } catch {
    // errorMessage jest ustawiany w useApplications()
  }
}

function startEditing(application: ParkingApplicationRead) {
  editingApplication.value = application
  successMessage.value = null
}

function cancelEditing() {
  editingApplication.value = null
}
</script>

<template>
  <section class="space-y-6">
    <div class="rounded-2xl border bg-white p-8 shadow-sm">
      <p class="text-sm font-medium uppercase tracking-wide text-blue-700">Panel użytkownika</p>

      <h1 class="mt-3 text-3xl font-bold tracking-tight text-slate-950">Moje wnioski parkingowe</h1>

      <p v-if="currentUser" class="mt-4 max-w-2xl text-slate-600">
        Zalogowano jako
        <span class="font-medium text-slate-900">
          {{ currentUser.first_name }} {{ currentUser.last_name }}
        </span>
        — {{ currentUser.email }}.
      </p>
    </div>

    <BaseAlert v-if="errorMessage" variant="error">
      {{ errorMessage }}
    </BaseAlert>
    <BaseAlert v-if="successMessage" variant="success">
      {{ successMessage }}
    </BaseAlert>

    <div class="grid gap-6 lg:grid-cols-[380px_1fr]">
      <aside class="space-y-6">
        <div class="rounded-2xl border bg-white p-6 shadow-sm">
          <h2 class="text-lg font-semibold text-slate-950">Nowy wniosek</h2>
          <p class="mt-2 text-sm text-slate-600">Złóż wniosek o dostęp do parkingu.</p>
          <div class="mt-5">
            <ApplicationForm
              submit-label="Utwórz wniosek"
              :pending="pending"
              @submit="submitCreateApplication"
              @cancel="() => null"
            />
          </div>
        </div>
        <div
          v-if="editingApplication"
          class="rounded-2xl border border-blue-200 bg-blue-50 p-6 shadow-sm"
        >
          <h2 class="text-lg font-semibold text-slate-950">Edycja wniosku</h2>
          <p class="mt-2 text-sm text-slate-600">
            Edytujesz wniosek:
            <span class="font-medium">
              {{ editingApplication.registration_number }}
            </span>
          </p>
          <div class="mt-5">
            <ApplicationForm
              submit-label="Zapisz zmiany"
              :pending="pending"
              :initial-registration-number="editingApplication.registration_number"
              :initial-preferred-floor="editingApplication.preferred_floor"
              @submit="submitUpdateApplication"
              @cancel="cancelEditing"
            />
          </div>
        </div>
      </aside>
      <div class="space-y-4">
        <div class="flex items-center justify-between">
          <div>
            <h2 class="text-lg font-semibold text-slate-950">Lista wniosków</h2>
            <p class="text-sm text-slate-600">Liczba wniosków: {{ applications.length }}</p>
          </div>
          <button
            type="button"
            class="rounded-lg border px-4 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-100"
            :disabled="pending"
            @click="loadMyApplications"
          >
            Odśwież
          </button>
        </div>
        <p v-if="pending && applications.length === 0" class="text-sm text-slate-500">
          Ładowanie wniosków...
        </p>
        <div
          v-else-if="applications.length === 0"
          class="rounded-2xl border border-dashed bg-white p-8 text-center text-sm text-slate-500"
        >
          Nie masz jeszcze żadnych wniosków parkingowych.
        </div>
        <div v-else class="space-y-4">
          <ApplicationCard
            v-for="application in applications"
            :key="application.id"
            :application="application"
            @edit="startEditing"
          />
        </div>
      </div>
    </div>
  </section>
</template>
