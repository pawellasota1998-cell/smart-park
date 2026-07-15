<script setup lang="ts">
import type { ApplicationStatus, ParkingApplicationRead } from '~/types/application'
definePageMeta({ middleware: 'supervisor' })

const {
  applications,
  pagination,
  filters,
  pending,
  errorMessage,
  loadApplications,
  approveApplication,
  rejectApplication,
  requestChanges,
  setStatusFilter,
  setRegistrationNumberFilter,
  setPage,
} = useSupervisorApplications()

const successMessage = ref<string | null>(null)
const selectedApplication = ref<ParkingApplicationRead | null>(null)
const decisionMode = ref<'reject' | 'request-changes' | null>(null)
const supervisorComment = ref('')

await loadApplications()
async function applyFilters() {
  successMessage.value = null
  await loadApplications()
}
async function clearFilters() {
  filters.value.status = ''
  filters.value.registration_number = ''
  filters.value.page = 1
  filters.value.sort_by = 'created_at'
  filters.value.sort_order = 'desc'

  await loadApplications()
}
async function goToPage(page: number) {
  setPage(page)
  await loadApplications()
}

async function approve(application: ParkingApplicationRead) {
  successMessage.value = null
  try {
    await approveApplication(application.id)
    successMessage.value = 'Wniosek został zaakceptowany.'
  } catch {
    // errorMessage ustawia composable
  }
}
function openDecisionModal(
  application: ParkingApplicationRead,
  mode: 'reject' | 'request-changes',
) {
  selectedApplication.value = application
  decisionMode.value = mode
  supervisorComment.value = ''
  successMessage.value = null
}

function closeDecisionModal() {
  selectedApplication.value = null
  decisionMode.value = null
  supervisorComment.value = ''
}

async function submitDecision() {
  if (!selectedApplication.value || !decisionMode.value) {
    return
  }

  successMessage.value = null

  try {
    if (decisionMode.value === 'reject') {
      await rejectApplication(selectedApplication.value.id, {
        supervisor_comment: supervisorComment.value || null,
      })
      successMessage.value = 'Wniosek został odrzucony.'
    }
    if (decisionMode.value === 'request-changes') {
      await requestChanges(selectedApplication.value.id, {
        supervisor_comment: supervisorComment.value,
      })

      successMessage.value = 'Wniosek został odesłany do poprawy.'
    }
    closeDecisionModal()
  } catch {
    // errorMessage ustawia composable
  }
}

function statusLabel(status: ApplicationStatus | '') {
  const labels: Record<ApplicationStatus, string> = {
    PENDING: 'Oczekujące',
    APPROVED: 'Zaakceptowane',
    REJECTED: 'Odrzucone',
    NEEDS_CHANGES: 'Do poprawy',
  }
  return status ? labels[status] : 'Wszystkie'
}

function canReview(application: ParkingApplicationRead) {
  return application.status === 'PENDING'
}
</script>

<template>
  <section class="space-y-6">
    <div class="rounded-2xl border bg-white p-8 shadow-sm">
      <p class="text-sm font-medium uppercase tracking-wide text-blue-700">Panel nadzorcy</p>
      <h1 class="mt-3 text-3xl font-bold tracking-tight text-slate-950">Wnioski parkingowe</h1>
      <p class="mt-4 max-w-2xl text-slate-600">
        Przeglądaj, filtruj i rozpatruj wnioski mieszkańców.
      </p>
    </div>
    <UiBaseAlert v-if="errorMessage" variant="error">
      {{ errorMessage }}
    </UiBaseAlert>

    <UiBaseAlert v-if="successMessage" variant="success">
      {{ successMessage }}
    </UiBaseAlert>
    <div class="rounded-2xl border bg-white p-6 shadow-sm">
      <h2 class="text-lg font-semibold text-slate-950">Filtry</h2>
      <div class="mt-5 grid gap-4 md:grid-cols-4">
        <div>
          <label class="text-sm font-medium text-slate-700" for="status"> Status </label>
          <select
            id="status"
            :value="filters.status"
            class="mt-1 w-full rounded-lg border px-3 py-2 text-sm"
            @change="
              setStatusFilter(($event.target as HTMLSelectElement).value as ApplicationStatus | '')
            "
          >
            <option value="">Wszystkie</option>
            <option value="PENDING">Oczekujące</option>
            <option value="APPROVED">Zaakceptowane</option>
            <option value="REJECTED">Odrzucone</option>
            <option value="NEEDS_CHANGES">Do poprawy</option>
          </select>
        </div>
        <div>
          <label class="text-sm font-medium text-slate-700" for="registration_number">
            Numer rejestracyjny
          </label>
          <input
            id="registration_number"
            :value="filters.registration_number"
            type="text"
            class="mt-1 w-full rounded-lg border px-3 py-2 text-sm"
            placeholder="np. WA"
            @input="setRegistrationNumberFilter(($event.target as HTMLInputElement).value)"
          />
        </div>

        <div>
          <label class="text-sm font-medium text-slate-700" for="sort_by"> Sortuj po </label>

          <select
            id="sort_by"
            v-model="filters.sort_by"
            class="mt-1 w-full rounded-lg border px-3 py-2 text-sm"
          >
            <option value="created_at">Dacie utworzenia</option>
            <option value="status">Statusie</option>
            <option value="registration_number">Numerze rejestracyjnym</option>
            <option value="preferred_floor">Piętrze</option>
          </select>
        </div>
        <div>
          <label class="text-sm font-medium text-slate-700" for="sort_order"> Kierunek </label>
          <select
            id="sort_order"
            v-model="filters.sort_order"
            class="mt-1 w-full rounded-lg border px-3 py-2 text-sm"
          >
            <option value="desc">Malejąco</option>
            <option value="asc">Rosnąco</option>
          </select>
        </div>
      </div>
      <div class="mt-5 flex gap-3">
        <button
          type="button"
          class="rounded-lg bg-gray-400 px-4 py-2 text-sm font-semibold text-white hover:bg-gray-500"
          :disabled="pending"
          @click="applyFilters"
        >
          Zastosuj
        </button>
        <button
          type="button"
          class="rounded-lg border px-4 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-100"
          :disabled="pending"
          @click="clearFilters"
        >
          Wyczyść
        </button>
      </div>
    </div>
    <div class="rounded-2xl border bg-white shadow-sm">
      <div class="flex items-center justify-between border-b px-6 py-4">
        <div>
          <h2 class="text-lg font-semibold text-slate-950">Lista wniosków</h2>

          <p class="text-sm text-slate-600">
            Status: {{ statusLabel(filters.status) }}, razem: {{ pagination.total_items }}
          </p>
        </div>

        <button
          type="button"
          class="rounded-lg border px-4 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-100"
          :disabled="pending"
          @click="loadApplications"
        >
          Odśwież
        </button>
      </div>
      <p v-if="pending && applications.length === 0" class="p-6 text-sm text-slate-500">
        Ładowanie wniosków...
      </p>
      <div v-else-if="applications.length === 0" class="p-8 text-center text-sm text-slate-500">
        Brak wniosków dla wybranych filtrów.
      </div>
      <div v-else class="overflow-x-auto">
        <table class="min-w-full divide-y divide-slate-200 text-sm">
          <thead
            class="bg-slate-50 text-left text-xs font-semibold uppercase tracking-wide text-slate-500"
          >
            <tr>
              <th class="px-6 py-3">ID</th>
              <th class="px-6 py-3">Numer</th>
              <th class="px-6 py-3">Piętro</th>
              <th class="px-6 py-3">Status</th>
              <th class="px-6 py-3">Komentarz</th>
              <th class="px-6 py-3 text-center">Akcje</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100 bg-white">
            <tr v-for="application in applications" :key="application.id">
              <td class="px-6 py-4 font-medium text-slate-900">{{ application.id }}</td>
              <td class="px-6 py-4">
                {{ application.registration_number }}
              </td>
              <td class="px-6 py-4">
                {{ application.preferred_floor }}
              </td>
              <td class="px-6 py-4">
                <UiApplicationStatusBadge :status="application.status" />
              </td>
              <td class="max-w-xs px-6 py-4 text-slate-600">
                {{ application.supervisor_comment || '—' }}
              </td>
              <td class="px-6 py-4">
                <div class="flex justify-end gap-2">
                  <button
                    type="button"
                    class="rounded-lg bg-green-700 px-3 py-1.5 text-xs font-semibold text-white hover:bg-green-800 disabled:cursor-not-allowed disabled:opacity-50"
                    :disabled="!canReview(application) || pending"
                    @click="approve(application)"
                  >
                    Akceptuj
                  </button>
                  <button
                    type="button"
                    class="rounded-lg bg-red-700 px-3 py-1.5 text-xs font-semibold text-white hover:bg-red-800 disabled:cursor-not-allowed disabled:opacity-50"
                    :disabled="!canReview(application) || pending"
                    @click="openDecisionModal(application, 'reject')"
                  >
                    Odrzuć
                  </button>
                  <button
                    type="button"
                    class="rounded-lg border px-3 py-1.5 text-xs font-semibold text-slate-700 hover:bg-slate-100 disabled:cursor-not-allowed disabled:opacity-50"
                    :disabled="!canReview(application) || pending"
                    @click="openDecisionModal(application, 'request-changes')"
                  >
                    Do poprawy
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="flex items-center justify-between border-t px-6 py-4 text-sm">
        <p class="text-slate-600">
          Strona {{ pagination.page }} z {{ pagination.total_pages || 1 }}
        </p>

        <div class="flex gap-2">
          <button
            type="button"
            class="rounded-lg border px-3 py-1.5 font-medium text-slate-700 hover:bg-slate-100 disabled:cursor-not-allowed disabled:opacity-50"
            :disabled="pagination.page <= 1 || pending"
            @click="goToPage(pagination.page - 1)"
          >
            Poprzednia
          </button>
          <button
            type="button"
            class="rounded-lg border px-3 py-1.5 font-medium text-slate-700 hover:bg-slate-100 disabled:cursor-not-allowed disabled:opacity-50"
            :disabled="pagination.page >= pagination.total_pages || pending"
            @click="goToPage(pagination.page + 1)"
          >
            Następna
          </button>
        </div>
      </div>
    </div>

    <div
      v-if="selectedApplication && decisionMode"
      class="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/50 p-4"
    >
      <div class="w-full max-w-lg rounded-2xl bg-white p-6 shadow-xl">
        <h2 class="text-lg font-semibold text-slate-950">
          {{ decisionMode === 'reject' ? 'Odrzuć wniosek' : 'Odeślij wniosek do poprawy' }}
        </h2>
        <p class="mt-2 text-sm text-slate-600">
          Wniosek {{ selectedApplication.id }} —
          {{ selectedApplication.registration_number }}
        </p>
        <div class="mt-5">
          <label class="text-sm font-medium text-slate-700" for="supervisor_comment">
            Komentarz
          </label>
          <textarea
            id="supervisor_comment"
            v-model="supervisorComment"
            rows="4"
            class="mt-1 w-full rounded-lg border px-3 py-2 text-sm outline-none focus:border-blue-600 focus:ring-2 focus:ring-blue-100"
            :required="decisionMode === 'request-changes'"
            placeholder="Wpisz komentarz dla użytkownika"
          />
        </div>
        <div class="mt-6 flex justify-end gap-3">
          <button
            type="button"
            class="rounded-lg border px-4 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-100"
            @click="closeDecisionModal"
          >
            Anuluj
          </button>
          <button
            type="button"
            class="rounded-lg bg-blue-700 px-4 py-2 text-sm font-semibold text-white hover:bg-blue-800 disabled:cursor-not-allowed disabled:opacity-60"
            :disabled="pending || (decisionMode === 'request-changes' && !supervisorComment.trim())"
            @click="submitDecision"
          >
            Zapisz decyzję
          </button>
        </div>
      </div>
    </div>
  </section>
</template>
